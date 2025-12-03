from dataclasses import dataclass

@dataclass
class Sentiero:
    idSentiero: int
    id1: int
    id2: int


    def __eq__(self, other):
        return isinstance(other, Sentiero) and self.idSentiero == other.idSentiero

    def __hash__(self):
        return hash(self.idSentiero)
