class Player:
    def __init__(self, id: str, name: str, strength: id):
        self._id = id
        self._name = name
        self._strength = strength

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def strength(self):
        return self._strength

    def __str__(self):
        return f"Player(id={self.id}, name={self.name}, strength={self.strength})"
