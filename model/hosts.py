class Host():
    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name.lower()

    def __str__(self):
        return f"""\nHost(id={self.id},
        name={self.name})"""
