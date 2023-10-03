from db.es.es_repository import EsRepository


class HackableRepository(EsRepository):

    def __init__(self, es):
        super().__init__(es, "index")

    def search(self, name: str):
        responses = self.es.search(index="entity", query={
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "fields": ["type"],
                                "query": "hackable"
                            }
                        },
                        {
                            "query_string": {
                                "fields": ["name"],
                                "query": f"\"{name}\""
                            }
                        },
                        {
                            "query_string": {
                                "fields": ["name"],
                                "query": f"\"{name}\""
                            }
                        }
                    ],
                    "should": [

                    ]
                }
            }
        )
        return [x["_source"] for x in responses["hits"]["hits"]]
