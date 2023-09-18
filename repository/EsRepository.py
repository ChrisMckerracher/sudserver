class EsRepository:
    def __init__(self, es):
        self.es = es

    def save(self, id, document):
        self.es.index(index="entity", id=id, document=document)