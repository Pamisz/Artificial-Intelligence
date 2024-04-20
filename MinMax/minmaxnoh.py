import math
from copy import deepcopy


class MinMaxAgentNoh:
    def __init__(self, token, depth=3):
        self.token = token
        self.depth = depth

    def decide(self, game):
        best_score = -math.inf
        best_move = -1
        for move in game.possible_drops():
            game_copy = deepcopy(game)
            game_copy.drop_token(move)
            score = self.min_max(game_copy, self.depth - 1, 0)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def min_max(self, game, depth, maximizing_player):
        if game._check_game_over():
            if game.wins == self.token:
                return 1
            elif game.wins is None:
                return 0
            else:
                return -1

        if depth == 0:
            return self.evaluate(game)

        best_score = -math.inf if maximizing_player else math.inf
        for move in game.possible_drops():
            game_copy = deepcopy(game)
            game_copy.drop_token(move)
            score = self.min_max(game_copy, depth - 1, not maximizing_player)
            if maximizing_player:
                if score > best_score:
                    best_score = score
            else:
                if score < best_score:
                    best_score = score
        return best_score

    def evaluate(self, game):
        for four in game.iter_fours():
            if four.count(self.token) == 4:
                return 1
            if four.count('x' if self.token == 'o' else 'o') == 4:
                return -1
        return 0
