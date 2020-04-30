import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Card:
    rank: str
    suit: str


@dataclass
class Move:
    piles: List[Card]
    start_index: int
    end_index: int


class Deck:  # each deck is its own class
    card_list = []
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def __init__(self):
        for suit in self.suits:
            for rank in self.ranks:
                c = Card(rank, suit)
                self.card_list.append(c)

    def shuffle(self):
        random.shuffle(self.card_list)


def cards_match(card1: Card, card2: Card) -> bool:
    return (card1.rank == card2.rank) or (card1.suit == card2.suit)


def can_move(piles: List[Card]):
    return len(get_possible_moves(piles)) == 0


def get_possible_moves(piles):
    moves = []
    for i in range(len(piles) - 1, 0, -1):
        if i >= 3:
            if cards_match(piles[i], piles[i - 3]):
                moves.append(Move(piles, start_index=i, end_index=i - 3))
        if cards_match(piles[i], piles[i - 1]):
            moves.append(Move(piles, start_index=i, end_index=i - 1))
    return moves


def get_all_moves(piles: List[Card]):
    moves_stack = [[move] for move in get_possible_moves(piles)]
    all_moves = []
    while moves_stack:
        move_list = moves_stack.pop()
        last_move = move_list[-1]
        new_piles = apply_move(last_move)
        new_moves = get_possible_moves(new_piles)
        if new_moves:
            for new_move in new_moves:
                to_add = move_list.copy()
                to_add.append(new_move)
                moves_stack.append(to_add)

        else:
            all_moves.append(move_list)
    return all_moves


def apply_move(move: Move) -> List[Card]:
    new_piles = move.piles.copy()
    new_piles[move.end_index] = new_piles[move.start_index]
    del new_piles[move.start_index]
    return new_piles


def apply_move_list(move_list):
    last_move = move_list[-1]
    piles = apply_move(last_move)
    return piles


def test_get_possible_moves():
    print(get_possible_moves(
        [Card("A", "Spades"), Card("A", "Hearts"), Card("4", "Spades"), Card("6", "Spades"), Card("A", "Clubs")]))


def test_get_all_moves():
    all_moves = get_all_moves(
        [Card("A", "Spades"), Card("A", "Hearts"), Card("4", "Spades"), Card("6", "Spades"), Card("A", "Clubs")])
    print(all_moves)


def test_apply_move_list():
    all_moves = get_all_moves(
        [Card("A", "Spades"), Card("A", "Hearts"), Card("4", "Spades"), Card("6", "Spades"), Card("A", "Clubs")])
    for move_list in all_moves:
        print(apply_move_list(move_list))


if __name__ == "__main__":
    test_get_all_moves()
    test_apply_move_list()
