from location.location_repository import LocationRepository
from query.query_service import QueryService


class LocationQueryService(QueryService):
    def __init__(self, repository: LocationRepository):
        super().__init__(repository)

    def query(self, fields):
        values = []
        values += self.repository.search(fields["locationType"], fields["name"])
        return values
