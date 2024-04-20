import math
from copy import deepcopy


class MinMaxAgent():
    def __init__(self, token, depth=3):
        self.token = token
        self.depth = depth

    def decide(self, game):
        return self.min_max(game, self.depth, 1)

    def min_max(self, game, depth, maximizing_player):
        if game._check_game_over:
            if game.wins == self.token:
                return 1
            elif game.wins == None:
                return 0
            else:
                return -1

        if depth == 0:
            return self.evaluate(game)

        best_score = -math.inf if maximizing_player else math.inf
        best_move = -1
        for move in game.possible_drops():
            game_copy = deepcopy(game)
            game_copy.drop_token(move)
            score = self.min_max(game_copy, depth - 1, not maximizing_player)
            if maximizing_player:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        return best_move

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
            if four.count(self.token) == 4:  # Gracz wygrywa
                score = 1
                break
            elif four.count(self.token) == 3 and four.count(
                    '_') == 1:  # Gracz ma trzy w rzędzie z jednym wolnym miejscem
                score += 0.2
            elif four.count(self.token) == 2 and four.count(
                    '_') == 2:  # Gracz ma dwie w rzędzie z dwoma wolnymi miejscami
                score += 0.1
            elif four.count(self.token) == 1 and four.count(
                    '_') == 3:  # Gracz ma jedną w rzędzie z trzema wolnymi miejscami
                score += 0.01

            if four.count('x' if self.token == 'o' else 'o') == 4:  # Przeciwnik wygrywa
                score = -1
                break
            elif four.count('x' if self.token == 'o' else 'o') == 3 and four.count(
                    '_') == 1:  # Przeciwnik ma trzy w rzędzie z jednym wolnym miejscem
                score -= 0.2
            elif four.count('x' if self.token == 'o' else 'o') == 2 and four.count(
                    '_') == 2:  # Przeciwnik ma dwie w rzędzie z dwoma wolnymi miejscami
                score -= 0.1
            elif four.count('x' if self.token == 'o' else 'o') == 1 and four.count(
                    '_') == 3:  # Przeciwnik ma jedną w rzędzie z trzema wolnymi miejscami
                score -= 0.01
        return score
