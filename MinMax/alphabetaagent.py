import math

class AlphaBetaAgent:
    def __init__(self, token, depth=3):
        self.token = token
        self.depth = depth

    def decide(self, game):
        possible_moves = game.possible_drops()
        best_move = None
        alpha = -math.inf
        beta = math.inf

        for move in possible_moves:
            game_copy = game.copy()
            game_copy.drop_token(move)
            score = self.alphabeta(game_copy, self.depth, alpha, beta, maximizing_player=False if self.token == 'x' else True)

            if (self.token == 'x' and score > alpha) or (self.token == 'o' and score < beta):
                alpha = score
                best_move = move

        return best_move

    def alphabeta(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game._check_game_over():
            return self.evaluate(game)

        if maximizing_player:
            v = -math.inf
            for move in game.possible_drops():
                game_copy = game.copy()
                game_copy.drop_token(move)
                v = max(v, self.alphabeta(game_copy, depth - 1, alpha, beta, maximizing_player=False))
                alpha = max(alpha, v)
                if v >= beta:
                    break  # β cutoff
            return v
        else:
            v = math.inf
            for move in game.possible_drops():
                game_copy = game.copy()
                game_copy.drop_token(move)
                v = min(v, self.alphabeta(game_copy, depth - 1, alpha, beta, maximizing_player=True))
                beta = min(beta, v)
                if v <= alpha:
                    break  # α cutoff
            return v

    def evaluate(self, game):
        score = 0
        for four in game.iter_fours():
            if four.count(self.token) == 4:  # Gracz wygrywa
                score += 1000
            elif four.count(self.token) == 3 and four.count('_') == 1:  # Gracz ma trzy w rzędzie z jednym wolnym miejscem
                score += 100
            elif four.count(self.token) == 2 and four.count('_') == 2:  # Gracz ma dwie w rzędzie z dwoma wolnymi miejscami
                score += 10
            elif four.count(self.token) == 1 and four.count('_') == 3:  # Gracz ma jedną w rzędzie z trzema wolnymi miejscami
                score += 1

            if four.count('x' if self.token == 'o' else 'o') == 4:  # Przeciwnik wygrywa
                score -= 1000
            elif four.count('x' if self.token == 'o' else 'o') == 3 and four.count('_') == 1:  # Przeciwnik ma trzy w rzędzie z jednym wolnym miejscem
                score -= 100
            elif four.count('x' if self.token == 'o' else 'o') == 2 and four.count('_') == 2:  # Przeciwnik ma dwie w rzędzie z dwoma wolnymi miejscami
                score -= 10
            elif four.count('x' if self.token == 'o' else 'o') == 1 and four.count('_') == 3:  # Przeciwnik ma jedną w rzędzie z trzema wolnymi miejscami
                score -= 1
        return score
