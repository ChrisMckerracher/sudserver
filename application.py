# DB
from datetime import datetime, timedelta
from typing import Optional
from urllib import request

import flask
from elasticsearch import Elasticsearch
from flask import Flask, redirect, url_for, make_response, jsonify
from flask import request, g
from flask_cors import CORS
from flask_pydantic import validate
from pydantic import BaseModel

from creature.creature_query_service import CreatureQueryService
from creature.creature_repository import CreatureRepository
from noauth.db.redis.client_builder import get_client
from emails.email_query_service import EmailQueryService
from emails.email_repository import EmailRepository
from hackable.hackable_repository import HackableRepository
from hackable.hacking_service import HackingService
from noauth.iam.access.access_management import is_authorized, is_socket_authorized
from noauth.iam.session.model.session import Session
from noauth.iam.user.model.user import User
from noauth.iam.user.model.user_role import UserRole
from noauth.iam.user.repository.user_repository import UserRepository
from location.location_query_service import LocationQueryService
from location.location_repository import LocationRepository
from flask_socketio import SocketIO, emit, join_room, disconnect, send

application = Flask("application",
                    static_url_path='',
                    static_folder='common/static',
                    template_folder='common/templates'
                    )
CORS(application, supports_credentials=True)
socketio = SocketIO(application)


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
# move this to a constants/config
session_cookie_name = "auth_session"
# we dont care about signing the jwt as security is a non issue, hell we dont even have true auth. this isn't really a pub key tehnically its a symmetric private key
public_key = "lol"
algo = "HS256"


@application.before_request
def is_authenticated():
    session_cookie = request.cookies.get(session_cookie_name)

    if (session_cookie):
        session = jwt.decode(session_cookie, public_key, algorithms=algo)
        session = Session.query(get_client()).get(session["session"])

        if (session):
            g.user = user_repository.get(session.user_id)
            # ToDo: some user validation shit the session could be mumbo jumbo
            return
    redirect(url_for("login"))


import jwt


@application.route('/login', methods=['POST'])
@validate()
def login():
    data = request.json
    name = data['name']
    role = data.get("role", UserRole.PLAYER)
    role = UserRole(role)

    user = user_repository.get(name)
    if not user:
        # admin will be manually created so for now new users are auto-player
        user = User(id=name, role=role)
        user_repository.save(id=name, document=user)

    # we manually just overwrite existing sessions atm since this app isn't meant to scale
    secrets_string = gen_secret()
    session = Session(id=secrets_string, user_id=user.id)
    Session.query(get_client()).save(session)
    token = jwt.encode({
        "session": secrets_string
    }, public_key, algorithm=algo)

    # long session time to be setup based on game length * 2 to be safe
    # ToDo: if running where ppl are not on same timezone, specify UTC for universality :^)
    expiration = datetime.now() + timedelta(hours=8)

    response = make_response(jsonify(message='Welcome Hacker 😎'))
    response.set_cookie(key=session_cookie_name, value=token, expires=expiration)
    # generic 200 for now
    return (response, 200)


import secrets


def gen_secret() -> str:
    # there's going to be like no users, we could probably even just do 1 btyte
    return secrets.token_urlsafe(4)


# todo: fix it so we're passing a pydantic model properly to actually validate
@application.route('/search', methods=['POST'])
@validate()
@is_authorized(UserRole.PLAYER)
# todo: fix it so we're passing a pydantic model properly to actually validate
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


@socketio.on("authenticate")
# ToDo: proper IAM support, proper pydantic validation
# ToDo: proper socket session management
def authenticate(message):
    if not message:
        disconnect(request.sid)
        return
    # At least for now, session auth is managed through http login
    # which i kinda like but i need to feel out if i should do socket auth sessions separatetly, probably not
    session_str = message['session']

    user = validate_socket_message(session_str)
    if not user:
        disconnect(request.sid, silent=True)
        return
    else:
        if user.role is UserRole.ADMIN:
            join_room(room="admin", sid=request.sid)
        # ToDo: test if flask-socketio forks sessions properly
        flask.session['user'] = user


@socketio.on("socketTest")
# ToDo: proper IAM support, proper pydantic validation
# ToDo: proper socket session management
@is_socket_authorized(UserRole.ADMIN)
def connect(message):
    user = flask.session['user']
    return


@socketio.on("rp_request")
# ToDo: proper IAM support, proper pydantic validation
# ToDo: proper socket session management
def rp_request(message):
    user = flask.session['user']
    rp_request_obj = message["request"]
    emit("rp_request", {
        "message": {
            "test": "test"
        },
        "request": rp_request_obj,
        "user": request.sid
    }, to="admin")


@socketio.on("rp_response")
@is_socket_authorized(UserRole.ADMIN)
def rp_response(message):
    sid = message["sid"]
    response = message["response"]
    emit("rp_response", {
        "response": response
    }, to=sid)


# ToDo Proper event code rather than these hardcoded yuckers
# ToDo Proper typing rather than these bare jsons
def validate_socket_message(session_str: str) -> Optional[User]:
    session = jwt.decode(session_str, public_key, algorithms=algo)
    session = Session.query(get_client()).get(session["session"])

    if (session):
        return user_repository.get(session.user_id)
    return None


if __name__ == '__main__':
    socketio.run(application, allow_unsafe_werkzeug=True, debug=True, port=8000)
