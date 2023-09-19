from hackable.HackableRepository import HackableRepository


class HackingService:

    def __init__(self, repository: HackableRepository):
        self.repository = repository

    def attemptHack(self, name):
        return self.repository.search(name)

    def hack(self, name, value):
        self.repository.save(name, value)