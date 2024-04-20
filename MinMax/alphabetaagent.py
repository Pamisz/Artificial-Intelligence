import math
from copy import deepcopy


class AlphaBetaAgent:
    def __init__(self, token, depth=3):
        self.token = token
        self.depth = depth

    def decide(self, game):
        possible_moves = game.possible_drops()
        best_move = -1
        alpha = -math.inf
        beta = math.inf
        best_score = -math.inf

        for move in possible_moves:
            game_copy = deepcopy(game)
            game_copy.drop_token(move)
            score = self.alphabeta(game_copy, self.depth - 1, alpha, beta, 0)

            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
        return best_move

    def alphabeta(self, game, depth, alpha, beta, maximizing_player):
        if game._check_game_over():
            if game.wins == self.token:
                return 1
            elif game.wins is None:
                return 0
            else:
                return -1

        if depth == 0:
            return self.evaluate(game)

        v = -math.inf if maximizing_player else math.inf
        for move in game.possible_drops():
            game_copy = deepcopy(game)
            game_copy.drop_token(move)
            if maximizing_player:
                v = max(v, self.alphabeta(game_copy, depth - 1, alpha, beta, 0))
                alpha = max(alpha, v)
                if v >= beta:
                    break
            else:
                v = min(v, self.alphabeta(game_copy, depth - 1, alpha, beta, 1))
                beta = min(beta, v)
                if v <= alpha:
                    break

        return v

    def evaluate(self, game):
        score = 0
        board = game.center_column()
        if self.token == "x":
            enemy_token = "o"
        else:
            enemy_token = "x"

        for i in range(len(board)):
            if board[i] == self.token:
                score += 0.1
            elif board[i] == enemy_token:
                score -= 0.1

        for four in game.iter_fours():
            if four.count(self.token) == 4:
                score = 1
                break
            elif four.count(self.token) == 3 and four.count('_') == 1:
                score += 0.2
            elif four.count(self.token) == 2 and four.count(
                    '_') == 2:
                score += 0.1
            elif four.count(self.token) == 1 and four.count(
                    '_') == 3:
                score += 0.01

            elif four.count(enemy_token) == 4:
                score = -1
                break
            elif four.count(enemy_token) == 3 and four.count(
                    '_') == 1:
                score -= 0.2
            elif four.count(enemy_token) == 2 and four.count(
                    '_') == 2:
                score -= 0.1
            elif four.count(enemy_token) == 1 and four.count(
                    '_') == 3:
                score -= 0.01
        return score
