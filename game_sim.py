from dataclasses import dataclass
from typing import List, Tuple

from game_logic import Card, Move, apply_move_list, Deck
from strategies import GameStrategy, GreedyStrategy, MinimaxStrategy


@dataclass
class GameResult:
    num_final_piles: int
    final_piles: List[Card]
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

    greedy = GreedyStrategy()
    minimax = MinimaxStrategy(max_depth=5)
    games_until_win = 0
    won = False
    while not won:
        games_until_win += 1
        d = Deck()
        d.shuffle()
        res = run_game(d.card_list, greedy)
        if res.num_final_piles == 1:
            won = True
    print(games_until_win)
    print(res)
