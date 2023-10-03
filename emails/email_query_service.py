from creature import CreatureRepository
from emails.EmailRepository import EmailRepository
from query.queryService import QueryService


class EmailQueryService(QueryService):
    def __init__(self, repository: EmailRepository):
        super().__init__(repository)

    def query(self, fields):
        values = []
        values += self.repository.search(fields["name"])
        return values
