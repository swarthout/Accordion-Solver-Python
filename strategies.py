import random
from abc import ABC
from typing import List

import numpy as np

from game_logic import Move, Card, get_all_moves, get_possible_moves, apply_move_list, apply_move
from minimax import MiniMax


class GameStrategy(ABC):

    def choose_move(self, piles: List[Card], deck: List[Card]) -> List[Move]:
        pass


class MinimaxStrategy(GameStrategy):

    def choose_move(self, piles: List[Card], deck: List[Card]) -> List[Move]:
        chosen_move_list = []
        all_moves = get_all_moves(piles)
        min_v = np.inf
        for move_list in all_moves:
            new_piles = apply_move_list(move_list)
            m = MiniMax()
            v = m.calculate(new_piles, deck, 4, -np.inf, np.inf, False)
            if v < min_v:
                min_v = v
                chosen_move_list = move_list
        return chosen_move_list


class GreedyStrategy(GameStrategy):
    def choose_move(self, piles: List[Card], deck: List[Card] = []) -> List[Move]:
        all_moves = get_all_moves(piles)
        min_piles = np.inf
        chosen_move_list = []
        for move_list in all_moves:
            resulting_piles = apply_move_list(move_list)
            num_piles = len(resulting_piles)
            if num_piles < min_piles:
                chosen_move_list = move_list
                min_piles = num_piles
        return chosen_move_list


class MoveOneStrategy(GameStrategy):
    def choose_move(self, piles: List[Card], deck: List[Card] = []) -> List[Move]:
        def is_move_one(move):
            return move.start_index - move.end_index == 1

        chosen_move_list = []
        possible_moves = get_possible_moves(piles)
        move_one_moves = list(filter(is_move_one, possible_moves))
        next_move = None
        if not possible_moves:
            return []
        elif move_one_moves:
            next_move = random.choice(move_one_moves)
        else:
            next_move = random.choice(possible_moves)
        while next_move:
            chosen_move_list.append(next_move)
            new_piles = apply_move(next_move)
            possible_moves = get_possible_moves(new_piles)
            move_one_moves = list(filter(is_move_one, possible_moves))
            if not possible_moves:
                next_move = None
            elif move_one_moves:
                next_move = random.choice(move_one_moves)
            else:
                next_move = random.choice(possible_moves)
        return chosen_move_list


class MoveThreeStrategy(GameStrategy):
    def choose_move(self, piles: List[Card], deck: List[Card] = []) -> List[Move]:
        def is_move_three(move):
            return move.start_index - move.end_index == 3

        chosen_move_list = []
        possible_moves = get_possible_moves(piles)
        move_three_moves = list(filter(is_move_three, possible_moves))
        next_move = None
        if not possible_moves:
            return []
        elif move_three_moves:
            next_move = random.choice(move_three_moves)
        else:
            next_move = random.choice(possible_moves)
        while next_move:
            chosen_move_list.append(next_move)
            new_piles = apply_move(next_move)
            possible_moves = get_possible_moves(new_piles)
            move_three_moves = list(filter(is_move_three, possible_moves))
            if not possible_moves:
                next_move = None
            elif move_three_moves:
                next_move = random.choice(move_three_moves)
            else:
                next_move = random.choice(possible_moves)
        return chosen_move_list


class RandomStrategy(GameStrategy):
    def choose_move(self, piles: List[Card], deck: List[Card] = []) -> List[Move]:
        all_moves = get_all_moves(piles)
        if not all_moves:
            return []
        return random.choice(all_moves)


if __name__ == "__main__":
    print(GreedyStrategy().choose_move(
        [Card("A", "Spades"), Card("A", "Hearts"), Card("4", "Spades"), Card("6", "Spades"), Card("A", "Clubs")]))
