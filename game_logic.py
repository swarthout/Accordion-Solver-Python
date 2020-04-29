from dataclasses import dataclass
from typing import List


@dataclass
class Card:
    rank: str
    suit: str


@dataclass
class Move:
    piles: List[Card]
    start_index: int
    end_index: int


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


def get_all_moves(piles):
    moves = get_possible_moves(piles)
    if not moves:
        return []
    all_moves = []
    for move in moves:
        new_piles = apply_move(move)
        new_moves = get_all_moves(new_piles)
        if new_moves:
            all_moves.append([move, new_moves])
        else:
            all_moves.append([move])
    return all_moves


def apply_move(move: Move) -> List[Card]:
    new_piles = move.piles.copy()
    new_piles[move.end_index] = new_piles[move.start_index]
    del new_piles[move.start_index]
    return new_piles


def test_get_possible_moves():
    print(get_possible_moves(
        [Card("A", "Spades"), Card("A", "Hearts"), Card("4", "Spades"), Card("6", "Spades"), Card("A", "Clubs")]))


def test_get_all_moves():
    all_moves = get_all_moves(
        [Card("A", "Spades"), Card("A", "Hearts"), Card("4", "Spades"), Card("6", "Spades"), Card("A", "Clubs")])
    print(list(all_moves))


if __name__ == "__main__":
    test_get_all_moves()
