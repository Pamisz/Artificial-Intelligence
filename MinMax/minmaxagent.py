import math
class MinMaxAgent():
    def __init__(self, token, depth=3):
        self.token = token
        self.depth = depth

    def decide(self, game):
        possible_moves = game.possible_drops()
        best_move = None
        best_score = -math.inf if self.token == 'x' else math.inf

        for move in possible_moves:
            game_copy = game.copy()
            game_copy.drop_token(move)
            score = self.min_max(game_copy, self.depth, False if self.token == 'x' else True)

            if (self.token == 'x' and score > best_score) or (self.token == 'o' and score < best_score):
                best_score = score
                best_move = move

        return best_move

    def min_max(self, game, depth, maximizing_player):
        if depth == 0 or game._check_game_over():
            return self.evaluate(game)

        if maximizing_player:
            max_eval = -math.inf
            for move in game.possible_drops():
                game_copy = game.copy()
                game_copy.drop_token(move)
                eval = self.min_max(game_copy, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for move in game.possible_drops():
                game_copy = game.copy()
                game_copy.drop_token(move)
                eval = self.min_max(game_copy, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval
        
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