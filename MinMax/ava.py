from exceptions import GameplayException
from connect4 import Connect4
from randomagent import RandomAgent
from minmaxagent import MinMaxAgent
from minmaxnoh import MinMaxAgentNoh
from alphabetaagent import AlphaBetaAgent

connect4 = Connect4(width=7, height=6)
buff = [RandomAgent('o'), MinMaxAgentNoh('x')] #random agent vs minmax with no heurystyka
buff2 = [MinMaxAgentNoh('o'), MinMaxAgent('x')] #minmax with no heurystyka vs minmax
buff3 = [MinMaxAgent('o'), AlphaBetaAgent('x')] #minmax vs alphabeta

while not connect4.game_over:
    connect4.draw()
    try:
        if connect4.who_moves == buff3[0].token:
            n_column = buff3[0].decide(connect4)
        else:
            n_column = buff3[1].decide(connect4)

        connect4.drop_token(n_column)
    except (ValueError, GameplayException):
        print('invalid move')

connect4.draw()
