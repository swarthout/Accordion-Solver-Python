import random
from typing import List
from game_logic import get_all_moves, apply_move_list, Card, Deck

import numpy as np


class MiniMax:
    num_simulated_draws = 10

    @staticmethod
    def eval_game_state(piles: List[Card]):
        return len(piles)

    def calculate(self, piles: List[Card], deck: List[Card], max_depth: int, alpha: int, beta: int, is_max: bool):
        # if the max depth has been exceeded, exit search
        if max_depth == 0:
            return self.eval_game_state(piles)
        # if the deck is empty the game is over, exit search
        if len(deck) == 0:
            return self.eval_game_state(piles)
        # if there are no moves to play, exit search
        if not get_all_moves(piles):
            return self.eval_game_state(piles)
        # this is the maximizing player (the one flipping new cards over)
        if is_max:
            children = []
            v = -np.inf
            # simulate num_simulated_draws
            for _ in range(self.num_simulated_draws):
                deck_copy = deck.copy()
                random.shuffle(deck_copy)
                piles_copy = piles.copy()
                card = deck_copy.pop(0)
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
            all_moves = get_all_moves(piles)
            v = np.inf
            for move in all_moves:
                child_pile = apply_move_list(move)
                v = min(v, self.calculate(child_pile, deck, max_depth - 1, alpha, beta, True))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v


if __name__ == "__main__":
    m = MiniMax()
    piles = [Card("A", "Spades"), Card("A", "Hearts"), Card("4", "Spades"), Card("6", "Spades"), Card("A", "Clubs")]
    deck = Deck()
    deck.shuffle()
    print(m.calculate(piles, deck.card_list, 4, -np.inf, np.inf, False))
