from creature.creature_repository import CreatureRepository
from query.query_service import QueryService


class CreatureQueryService(QueryService):
    def __init__(self, repository: CreatureRepository):
        super().__init__(repository)

    def query(self, fields):
        name = fields["name"]
        species = fields["species"]

        values = []

        if (name == ""):
            values += self.repository.search(species, "*")
            for value in values:
                if value["name"] == "":
                    value["name"] = "Info"
        elif (species == ""):
            values += self.repository.search("*", name)

        return values
