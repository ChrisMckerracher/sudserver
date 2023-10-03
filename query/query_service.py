class QueryService:

    def __init__(self, repository):
        self.repository = repository
    def query(self, fields):
        raise NotImplementedError()