from elasticsearch import Elasticsearch

from noauth.db.es.es_repository import EsRepository

es = Elasticsearch(hosts="http://0.0.0.0:9200")

class LocationRepository(EsRepository):

    def __init__(self, es):
        super().__init__(es, "index")

    def search(self, field: str, name: str):
        responses = self.es.search(index="location", query={
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "fields": ["type"],
                                "query": "location"
                            }
                        },
                        {
                            "query_string": {
                                "fields": ["locationType"],
                                "query": f"\"{field}\""
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
