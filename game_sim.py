from dataclasses import dataclass
from typing import List, Tuple

from game_logic import Card, Move, apply_move_list, Deck
from strategies import GameStrategy, GreedyStrategy


@dataclass
class GameResult:
    final_piles: List[Card]
    num_final_piles: int
    game_recording: List[Tuple[List[Card], List[Move]]]


def run_game(deck: List[Card], strategy: GameStrategy):
    piles = []
    result = GameResult(final_piles=[], num_final_piles=1, game_recording=[])
    while deck:
        top_card = deck.pop(0)
        piles.append(top_card)
        move_list = strategy.choose_move(piles, deck)
        result.game_recording.append((piles.copy(), move_list))
        if move_list:
            piles = apply_move_list(move_list)
    result.final_piles = piles
    result.num_final_piles = len(piles)
    return result


if __name__ == "__main__":

    s = GreedyStrategy()

    won = False
    while not won:
        d = Deck()
        d.shuffle()
        res = run_game(d.card_list, s)
        if res.num_final_piles == 1:
            won = True

    print(res)
