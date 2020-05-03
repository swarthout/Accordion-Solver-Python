from dataclasses import dataclass
from typing import List, Tuple

import numpy as np

from game_logic import Card, Move, apply_move_list, Deck
from strategies import GameStrategy, GreedyStrategy, MinimaxStrategy, OptimisticStrategy, RandomStrategy


@dataclass
class GameResult:
    num_final_piles: int
    final_piles: List[Card]
    game_recording: List[Tuple[List[Card], List[Move]]]

    def get_full_piles(self):
        piles = []
        for event in self.game_recording:
            recorded_piles, move_list = event
            piles.append([recorded_piles[-1]])
            for move in move_list:
                start = move.start_index
                end = move.end_index
                piles[end].extend(piles[start])
                del piles[start]

        return piles


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

def run_n_games(s, n, riffles=None):
    results = []
    d = Deck()
    d.shuffle()
    for i in range(n):
        res = run_game(d.card_list, s)
        results.append(res.num_final_piles)
        if riffles != None:
            d = Deck()
            d.reconstruct(res.get_full_piles())
            for j in range(riffles):
                d.riffle()
        else:
            d = Deck()
            d.shuffle()
    return results

if __name__ == "__main__":

    greedy = GreedyStrategy()
    random = RandomStrategy()
    minimax = MinimaxStrategy(max_depth=5)
    optimist = OptimisticStrategy()

    n = 200000
    #riffles = 12

    for t in range(5):
        results = run_n_games(random, n)
        results = np.array(results)
        np.save(f"random_strat_random_deck_t{t}.npy", results)

