from creature.creature_repository import CreatureRepository
from emails.email_repository import EmailRepository
from query.query_service import QueryService


class EmailQueryService(QueryService):
    def __init__(self, repository: EmailRepository):
        super().__init__(repository)

    def query(self, fields):
        values = []
        values += self.repository.search(fields["name"])
        return values
