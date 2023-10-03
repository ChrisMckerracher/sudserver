# DB
from urllib import request

from elasticsearch import Elasticsearch
from flask import Flask
from flask import request
from flask_cors import CORS
from flask_pydantic import validate
from pydantic import BaseModel

from creature.creature_query_service import CreatureQueryService
from creature.creature_repository import CreatureRepository
from emails.email_query_service import EmailQueryService
from emails.email_repository import EmailRepository
from hackable.hackable_repository import HackableRepository
from hackable.hacking_service import HackingService
from location.location_query_service import LocationQueryService
from location.location_repository import LocationRepository

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