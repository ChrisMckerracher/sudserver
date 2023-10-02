from elasticsearch import Elasticsearch

from repository.EsRepository import EsRepository

es = Elasticsearch(hosts="http://0.0.0.0:9200")


class UserRepository(EsRepository):

    def __init__(self, es):
        super().__init__(es, "user")

    def get(self, name: str):
        responses = self.es.search(index="user", query={
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "fields": ["name"],
                            "query": f"{name}"
                        }
                    }
                ],
                "should": [

                ]
            }
        }
                                   )
        return [x["_source"] for x in responses["hits"]["hits"]]
