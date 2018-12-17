import itertools
import random
from dataclasses import dataclass
# from enum import Enum
from typing import List

DIAMOND = "diamond"
GOLD = "gold"
SILVER = "silver"
CLOTH = "cloth"
SPICE = "spice"
LEATHER = "leather"

CAMEL = "camel"

# reward function teaches possible outcomes
BAD_MOVE = -100500
OK_MOVE = 0

# class Card(Enum):
#     DIAMOND = Enum.auto()
#     GOLD = Enum.auto()
#     SILVER = Enum.auto()
#     CLOTH = Enum.auto()
#     SPICE = Enum.auto()
#     LEATHER = Enum.auto()
#     CAMEL = Enum.auto()

CARD_VALUES = {
    DIAMOND: 6,
    GOLD: 5,
    SILVER: 4,
    CLOTH: 3,
    SPICE: 2,
    LEATHER: 1,
}

EXTRA_VALUES = {
    0: -9000,
    1: 0,
    2: 0,
    3: 2,
    4: 5,
    5: 9,
    6: 9,
    7: 9,
}


#     DIAMOND = Enum.auto()
#     GOLD = Enum.auto()
#     SILVER = Enum.auto()
#     CLOTH = Enum.auto()
#     SPICE = Enum.auto()
#     LEATHER = Enum.auto()
#     CAMEL = Enum.auto()


@dataclass
class State:
    deck: List[str]
    market: List[str]
    hand: List[str]
    enemyHand: List[str]
    camels: int = 0
    score: int = 0
    enemyCamels: int = 0
    enemyScore: int = 0

    def exchange_cards(self, to_take: List[str], to_give: List[str]) -> float:
        if len(to_give) != len(to_take):
            raise Exception
        if len(to_give) < 2:
            return BAD_MOVE
        for i in range(len(to_give)):
            if to_take[i] is CAMEL:
                self.camels += 1
                self.market[self.market.index(to_take[i])] = to_give[i]
            elif to_give[i] is CAMEL:
                if self.camels < 1:
                    raise Exception
                self.camels -= 1
                self.hand[self.hand.index(to_give[i])] = to_take[i]
            else:
                self.hand[self.hand.index(to_give[i])] = to_take[i]
                self.market[self.market.index(to_take[i])] = to_give[i]
                return OK_MOVE

    def take_1_single_good(self, index: int) -> float:
        if len(self.hand) > 6:
            return BAD_MOVE
        if self.market[index] is CAMEL:
            return BAD_MOVE
        self.hand.append(self.market[index])
        self.market[index] = self.deck.pop()
        return OK_MOVE

    def take_the_camels(self) -> float:
        for i, card in enumerate(self.market):
            if card is CAMEL:
                self.market[i] = self.deck.pop()
                self.camels += 1
        return OK_MOVE

    def sell_cards(self, index: int) -> float:
        """sell all cards of given value; it might be more efficient to sell 2 golds and keep 1"""
        if index >= len(self.hand):
            return BAD_MOVE
        card = self.hand[index]
        count = self.hand.count(card)
        if card in [DIAMOND, GOLD, SILVER]:
            if count < 2:
                return BAD_MOVE
        self.score += CARD_VALUES[card] * count + EXTRA_VALUES[count]
        return CARD_VALUES[card] * count + EXTRA_VALUES[count]

    def print(self):
        print("--------")
        print(self.enemyHand, "[camels:", str(self.enemyCamels) + "] [score: ", str(self.enemyScore) + "]", "[enemy]")
        print(self.market, "[market]")
        print(self.hand, "[camels:", str(self.camels) + "] [score: ", str(self.score) + "]", "[you]")
        print("--------")

    def flip_sides(self):
        return State(self.deck, self.market,
                     hand=self.enemyHand, enemyHand=self.hand,
                     score=self.enemyScore, enemyScore=self.score,
                     camels=self.enemyCamels, enemyCamels=self.camels,
                     )


def init_state() -> State:
    deck = list(itertools.chain(
        [DIAMOND] * 6,
        [GOLD] * 6,
        [SILVER] * 6,
        [CLOTH] * 8,
        [SPICE] * 8,
        [LEATHER] * 10,
        [CAMEL] * 8,
    ))
    random.shuffle(deck)
    # init market
    market = [CAMEL] * 3
    market.append(deck.pop())
    market.append(deck.pop())
    # deal 5 cards to each player
    player1 = []
    camels = 0
    player2 = []
    enemy_camels = 0
    for i in range(5):
        card = deck.pop()
        if card is CAMEL:
            camels += 1
        else:
            player1.append(card)
        card = deck.pop()
        if card is CAMEL:
            enemy_camels += 1
        else:
            player2.append(card)
    return State(deck, market, player1, player2, camels=camels, enemyCamels=enemy_camels)


def greedy_card_exchange(market, hand):
    """ Do not exchange camels for now """
    to_take = list()
    to_give = list()
    for handIndex, handCard in enumerate(hand):
        if handCard in [CLOTH, SPICE, LEATHER]:
            for marketIndex, marketCard in enumerate(market):
                if marketCard in [DIAMOND, GOLD, SILVER]:
                    to_take.append(market[marketIndex])
                    to_give.append(hand[handIndex])
    return to_take, to_give
