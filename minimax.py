import random
from typing import List

import numpy as np


class MiniMax:
    num_simulated_draws = 10

    @staticmethod
    def eval_game_state(piles: List):
        return len(piles)

    def calculate(self, piles: List, deck: List, max_depth: int, alpha: int, beta: int, is_max: bool):
        # if the max depth has been exceeded, exit search
        if max_depth == 0:
            return self.eval_game_state(piles)
        # if the deck is empty the game is over
        if len(deck) == 0:
            return self.eval_game_state(piles)
        # this is the maximizing player (the one flipping new cards over)
        if is_max:
            children = []
            v = -np.inf
            for _ in range(self.num_simulated_draws):
                deck_copy = deck.copy()
                random.shuffle(deck_copy)
                piles_copy = piles.copy()
                card = deck.pop()
                piles_copy.append(card)
                children.append((piles_copy, deck_copy))
            for child in children:
                v = max(v, self.calculate(child[0], child[1], max_depth - 1, alpha, beta, False))
                if v >= beta:
                    return v
                alpha = max(alpha, v)

            return v
        # this is the minimizing player (the one trying to collapse the deck to 1 pile)
        else:
            pass
