from noauth.db.es.es_repository import EsRepository

class CreatureRepository(EsRepository):

    def __init__(self, es):
        super().__init__(es, "index")

    def search(self, species: str, name: str):
        responses = self.es.search(index="creature", query={
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "fields": ["species"],
                            "query": f"{species}" if species == "*" or species == "" else f"\"{species}\""
                        }
                    },
                    {
                        "query_string": {
                            "fields": ["name"],
                            "query": f"{name}" if name == "*" or name == "" else f"\"{name}\""
                        }
                    }
                ],
                "should": [

                ]
            }
        }
                                   )
        return [x["_source"] for x in responses["hits"]["hits"]]
