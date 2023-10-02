from elasticsearch import Elasticsearch

from repository.EsRepository import EsRepository

es = Elasticsearch(hosts="http://0.0.0.0:9200")

class EmailRepository(EsRepository):

    def __init__(self, es):
        super().__init__(es, "index")

    def search(self, email: str):
        responses = self.es.search(index="entity", query={
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "fields": ["type"],
                                "query": "email"
                            }
                        },
                        {
                            "query_string": {
                                "fields": ["to", "from"],
                                "query": f"\"{email}\""
                            }
                        }
                    ],
                    "should": [

                    ]
                }
            }
        )
        return [x["_source"] for x in responses["hits"]["hits"]]

