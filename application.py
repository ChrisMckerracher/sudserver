# DB
from urllib import request

from elasticsearch import Elasticsearch
from flask import Flask
from flask_cors import CORS
from flask_pydantic import validate
from pydantic import BaseModel
from flask import g, request, render_template, redirect, send_from_directory

from creature.CreatureQueryService import CreatureQueryService
from creature.CreatureRepository import CreatureRepository

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

@application.route('/search', methods=['POST'])
@validate()
def search():
    data = request.json
    type = data["type"]
    response = []

    if type == "creature":
        response = creatureQueryService.query(data)


    response = {
        "values": response
    }

    response.update(data)

    return (response, 200)

if __name__ == '__main__':
    application.run(debug=True, port=8000)