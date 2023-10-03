
from elasticsearch import Elasticsearch


class EsRepository:
    def __init__(self, es: Elasticsearch, index: str):
        self.es = es
        self.index = index

    def save(self, id, document):
        self.es.index(index=self.index, id=id, document=document)