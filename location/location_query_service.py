from creature import CreatureRepository
from emails.EmailRepository import EmailRepository
from location.LocationRepository import LocationRepository
from query.queryService import QueryService


class LocationQueryService(QueryService):
    def __init__(self, repository: LocationRepository):
        super().__init__(repository)

    def query(self, fields):
        values = []
        values += self.repository.search(fields["locationType"], fields["name"])
        return values
