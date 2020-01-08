class UnknownTable(Exception):
    def __init__(self, missing: str):
        self.missing = missing

    def __str__(self):
        return str(self.missing)
