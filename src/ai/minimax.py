import random
from time import time
from typing import Tuple, List
from copy import deepcopy

from src.constant import ShapeConstant
from src.model import State, Board
from src.utility import place, check_streak

'''
Minimax Alpha Beta Pruning
'''
def getRow(state: State, n_player: int, shape: str, col: str) -> int:
    """
    Modification of place function, just remove set board state.
    [DESC]
        Function to get location of piece in board
    [PARAMS]
        state = current state in the game
        n_player = which player (player 1 or 2)
        shape = shape
        col = which col
    [RETURN]
        -1 if placement is invalid
        int(row) if placement is valid 
    """
    if state.players[n_player].quota[shape] == 0:
        return -1

    for row in range(state.board.row - 1, -1, -1):
        try:
            if state.board[row, col].shape == ShapeConstant.BLANK:
                return int(row)
        except Exception as e:
            pass

    return -1

def count_streak(board: Board, row: int, col: int) -> int:
    piece = board[row, col]
    if piece.shape == ShapeConstant.BLANK:
        return None

    streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    ret_count = 0
    for prior in GameConstant.WIN_PRIOR:
        mark = 0
        for row_ax, col_ax in streak_way:
            row_ = row + row_ax
            col_ = col + col_ax
            for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                if is_out(board, row_, col_):
                    mark = 0
                    break

                shape_condition = (
                    prior == GameConstant.SHAPE
                    and piece.shape != board[row_, col_].shape
                )
                color_condition = (
                    prior == GameConstant.COLOR
                    and piece.color != board[row_, col_].color
                )
                if shape_condition or color_condition:
                    mark = 0
                    break

                row_ += row_ax
                col_ += col_ax
                mark += 1

            if mark == GameConstant.N_COMPONENT_STREAK - 1:
                return mark
            elif mark > ret_count:
                ret_count = mark
    
    return ret_count

def score(state: State, n_player: int) -> int:
    board = state.board
    temp_win = -1
    for row in range(board.row):
        for col in range(board.col):
            if board[row,col].color == state.players[n_player].color: #mencocokan warna
                tmp_score = count_streak(board, row, col)
                if tmp_score>temp_win:
                    temp_win = tmp_score
                
                if temp_win==GameConstant.N_COMPONENT_STREAK - 1:
                    win = check_streak(board,row,col)
                    if win and win[0] == GameConstant.WIN_PRIOR[0]: #prioritas berdasar shape win 
                        return temp_win + 1
                    
    return temp_win

class Minimax:
    def __init__(self):
        self.thinking_time = 0
        self.best_movement = (random.randint(0, 6), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
    
    def getMoves(self, n_player, state: State) -> List[Tuple[str, str]]:
        """
        Menghasilkan list suksesor dari sebuah state board
        """
        moveList = []
        player = state.players[n_player]

        for i in range(7):
            if player.quota[ShapeConstant.CROSS] != 0:
                moveList.append((i, ShapeConstant.CROSS))

            if player.quota[ShapeConstant.CIRCLE] != 0:
                moveList.append((i, ShapeConstant.CIRCLE))

        return moveList

    def minimax(self, n_player: int, state: State, depth: int) -> Tuple[str, str]:
        # Inisialisasi alpha beta
        alpha = -1000
        nodeScore = -1000
        beta = 1000
        moveList = self.getMoves(n_player, state)
        
        for move in moveList:
            # Deep copy state and do move
            newState = deepcopy(state)
            valid = place(newState, n_player, move[1], move[0])

            if (valid != -1):
                # Get opponent action
                minValue = self.minABValue(newState, (n_player+1)%2, alpha, beta, depth+1)
                
                if minValue > alpha:
                    nodeScore = minValue
                    self.best_movement = move

                alpha = max(nodeScore, alpha)

        return self.best_movement

    def minABValue(self, state: State, n_player: int, alpha: int, beta: int, depth: int) -> int:
        """
        Cari skor minimum dengan melakukan aksi musuh. Mengembalikan skor.
        """
        nodeScore = 1000
        moveList = self.getMoves(n_player, state)

        for move in moveList:
            # Deep copy state and do move
            newState = deepcopy(state)
            valid = place(newState, n_player, move[1], move[0])
            # If placement valid, count nodeScore
            if (valid != -1):
                #print(newState.board)
                nodeScore = min(nodeScore, self.maxABValue(newState, (n_player+1)%2, alpha, beta, depth+1))
                # Prune
                if (nodeScore <= alpha):
                    return nodeScore

                beta = min(beta, nodeScore)

        return nodeScore

    def maxABValue(self, state: State, n_player: int, alpha: int, beta: int, depth: int) -> int:
        """
        Cari skor maksimum. Mengembalikan score
        """
        # Apabila node daun, kembalikan score node berdasarkan objective function
        if depth == 4:
            terminalScore = score(state, n_player)
            return terminalScore

        nodeScore = -1000
        moveList = self.getMoves(n_player, state)

        for move in moveList:
            # Deep copy state and do move
            newState = deepcopy(state)
            valid = place(newState, n_player, move[1], move[0])

            if (valid != -1):
                nodeScore = max(nodeScore, self.minABValue(newState, (n_player+1)%2, alpha, beta, depth+1))
                #if beta < nodeScore, prune
                if (nodeScore >= beta):
                    return nodeScore
                #update alpha
                alpha = max(alpha, nodeScore)

        return nodeScore

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        while (time() < self.thinking_time):
            self.minimax(n_player, state, 0)
            break #Break if finished exploring successor tree
            
        return self.best_movement

import random
from copy import deepcopy
from time import time

from src.utility import *
from src.model import State

from typing import Tuple, List


class Minimax2:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return best_movement
