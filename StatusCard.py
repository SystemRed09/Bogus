from json import loads
from dataclasses import dataclass

@dataclass
class StatusCard:
    type: str
    uID: str
    title: str

    @classmethod
    def fromJsonFile(cls, fileName: str, index=0) -> StatusCard:
        with open(fileName, 'r') as file:
            c = loads(file.read())[index]
            return StatusCard(c["type"], c["uniqueId"], c["IrTitle"])

    @classmethod
    def fromJson(cls, body: str, index=0) -> StatusCard:
        c = loads(body)[index]
        try: uid = c["uniqueId"]
        except KeyError: uid = "0"
        return StatusCard(c["type"], uid, c["IrTitle"])

    def print(self) -> None:
        print(f"Card {self.uID} of type {self.type} says {self.title}")