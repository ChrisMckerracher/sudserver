# DB
from urllib import request

from elasticsearch import Elasticsearch
from flask import Flask, redirect, url_for
from flask import request
from flask_cors import CORS
from flask_pydantic import validate
from pydantic import BaseModel

from creature.creature_query_service import CreatureQueryService
from creature.creature_repository import CreatureRepository
from db.redis.client_builder import get_client
from emails.email_query_service import EmailQueryService
from emails.email_repository import EmailRepository
from hackable.hackable_repository import HackableRepository
from hackable.hacking_service import HackingService
from iam.session.model.session import Session
from iam.user.repository.user_repository import UserRepository
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
creature_repository = CreatureRepository(es)
creature_query_service = CreatureQueryService(creature_repository)

email_repository = EmailRepository(es)
email_query_service = EmailQueryService(email_repository)

location_repository = LocationRepository(es)
location_query_service = LocationQueryService(location_repository)


user_repository = UserRepository(es, get_client())
#move this to a constants/config
session_cookie_name = "auth_session"
#we dont care about signing the jwt as security is a non issue, hell we dont even have true auth
public_key = "lol"
algo = "HS256"
@application.before_request()
def is_authenticated():
    session_cookie = request.cookies.get(session_cookie_name)

    if (session_cookie):
        session = Session.model_validate_json(session_cookie)
        session = Session.query(get_client()).get(session.id)

        if (session):
            g.user = user_repository.get(session.id)
            #ToDo: some user validation shit the session could be mumbo jumbo
            return
    redirect(url_for("/login"))




#todo: fix it so we're passing a pydantic model properly to actually validate
@application.route('/search', methods=['POST'])
@validate()
#todo: fix it so we're passing a pydantic model properly to actually validate
def search():
    data = request.json
    type = data["type"]
    response = []

    if type == "creature":
        response = creature_query_service.query(data)
    elif type == "email":
        response = email_query_service.query(data)
    elif type == "location":
        response = location_query_service.query(data)

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