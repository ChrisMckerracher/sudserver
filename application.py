# DB
from urllib import request

from elasticsearch import Elasticsearch
from flask import Flask
from flask import request
from flask_cors import CORS
from flask_pydantic import validate
from pydantic import BaseModel

from creature.CreatureQueryService import CreatureQueryService
from creature.CreatureRepository import CreatureRepository
from emails.EmailQueryService import EmailQueryService
from emails.EmailRepository import EmailRepository
from hackable.HackableRepository import HackableRepository
from hackable.HackingService import HackingService
from location.LocationQueryService import LocationQueryService
from location.LocationRepository import LocationRepository

application = Flask("application",
                    static_url_path='',
                    static_folder='common/static',
                    template_folder='common/templates'
                    )

CORS(application, supports_credentials=True)


class SearchBody(BaseModel):
    type: str


es = Elasticsearch(hosts="http://0.0.0.0:9200")
creatureRepository = CreatureRepository(es)
creatureQueryService = CreatureQueryService(creatureRepository)

emailRepository = EmailRepository(es)
emailQueryService = EmailQueryService(emailRepository)

locationRepository = LocationRepository(es)
locationQueryService = LocationQueryService(locationRepository)

#todo: fix it so we're passing a pydantic model properly to actually validate

@application.route('/search', methods=['POST'])
@validate()
#todo: fix it so we're passing a pydantic model properly to actually validate
def search():
    data = request.json
    type = data["type"]
    response = []

    if type == "creature":
        response = creatureQueryService.query(data)
    elif type == "email":
        response = emailQueryService.query(data)
    elif type == "location":
        response = locationQueryService.query(data)

    response = {
        "values": response
    }

    response.update(data)

    return (response, 200)


hackingRepository = HackableRepository(es)
hackingService = HackingService(hackingRepository)
@application.route('/hack', methods=['POST'])
@validate()
def hack():
    data = request.json

    response = hackingService.attemptHack(data["name"])

    response = {
        "values": response
    }

    response.update(data)

    return (response, 200)

@application.route('/login', methods=['POST'])
@validate()
def login():
    data = request.json
    name = data['name']




if __name__ == '__main__':
    application.run(debug=True, port=8000)