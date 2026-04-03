from Connection import Connection, ErrorCode
from StatusCard import StatusCard
from json import loads


class Printer:
    cards: list[StatusCard]
    name: str
    cable: Connection

    def __init__(self, ip4: str, name: str) -> None:
        self.name = name
        self.cards = []
        self.cable = Connection(ip4)
        if self.cable.error is None:
            self.jsonToCards()

    def jsonToCards(self) -> None:
        self.cards = []
        for i in range(self.cardCount):
            self.cards.append(StatusCard.fromJson(self.body, i))

    @property
    def cardCount(self) -> int:
        c = loads(self.body)
        if isinstance(c, list):
            return len(c)
        return 0

    @property
    def body(self) -> str:
        if self.cable.body is None:
            return ""
        return self.cable.body

    @property
    def error(self) -> ErrorCode | None:
        return self.cable.error

    def hasError(self) -> bool:
        return self.error is not None

    def printCards(self) -> None:
        for card in self.cards:
            card.print()

    def getWarnings(self) -> tuple[StatusCard, ...]:
        wCards = []
        for card in self.cards:
            if card.type == "warning":
                wCards.append(card)
        return tuple(wCards)

    def hasWarning(self) -> bool:
        for card in self.cards:
            if card.type == "warning":
                return True
        return False