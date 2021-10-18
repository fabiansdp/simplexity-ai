import random
from time import time
from typing import Tuple, List
from copy import deepcopy

from src.constant import ShapeConstant, GameConstant
from src.model import State, Board
from src.utility import place, is_out

'''
Minimax Alpha Beta Pruning
'''

def count_streak(board: Board, row: int, col: int) -> int:
    piece = board[row, col]
    if piece.shape == ShapeConstant.BLANK:
        return None

    # Arah mata angin
    streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    ret_count = 1
    # Loop prioritas kemenangan yaitu shape dulu baru color
    for prior in GameConstant.WIN_PRIOR:
        mark = 1
        # Pergerakan arah mata angin
        for row_ax, col_ax in streak_way:
            row_ = row + row_ax
            col_ = col + col_ax
            # Gerakan sebanyak 4 kali
            for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                # Apabila posisi di luar board, break
                if is_out(board, row_, col_):
                    break

                # Apabila saat pengecekan streak shape dan piece bukan shape yang sama
                shape_condition = (
                    prior == GameConstant.SHAPE
                    and piece.shape != board[row_, col_].shape
                )
                # Apabila saat pengecekan streak color dan piece pada board bukan color yang sama
                color_condition = (
                    prior == GameConstant.COLOR
                    and piece.color != board[row_, col_].color
                )
                # Apabila terjadi salah satu dari kedua kondisi di atas, break
                if shape_condition or color_condition:
                    break

                row_ += row_ax
                col_ += col_ax
                mark += 1

            if mark > ret_count:
                ret_count = mark

            # Apabila ada streak berjumlah 4, langsung return
            if mark == GameConstant.N_COMPONENT_STREAK:
                return mark
    
    return ret_count

def score(state: State, n_player: int) -> int:
    board = state.board
    stateScore = 0
    # Penelusuran seluruh kolom dan baris
    for row in range(board.row):
        for col in range(board.col):
            # Apabila warna bidak sama dengan warna pemain, mulai penghitungan streak
            if board[row,col].color == state.players[n_player].color:
                tempScore = count_streak(board, row, col)
                if tempScore > stateScore:
                    stateScore = tempScore
                
    return stateScore

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
        # Get move list
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