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
def maxScore(tuple1: Tuple[str, int], tuple2: Tuple[str, int]) -> Tuple[str, int]:
    if scoreGreater(tuple1, tuple2):
        return tuple1
    
    if scoreGreater(tuple2, tuple1):
        return tuple2

    return tuple1

def minScore(tuple1: Tuple[str, int], tuple2: Tuple[str, int]) -> Tuple[str, int]:
    if scoreSmaller(tuple1, tuple2):
        return tuple1
    
    if scoreSmaller(tuple2, tuple1):
        return tuple2

    return tuple1

def scoreGreater(tuple1: Tuple[str, int], tuple2: Tuple[str, int]) -> bool:
    if tuple1[1] > tuple2[1]:
        return True
    
    if tuple1[1] == tuple2[1] and tuple1[0] == GameConstant.WIN_PRIOR[0]:
        return True

    return False

def scoreSmaller(tuple1: Tuple[str, int], tuple2: Tuple[str, int]) -> bool:
    if tuple1[1] < tuple2[1]:
        return True
    
    if tuple1[1] == tuple2[1] and tuple1[0] == GameConstant.WIN_PRIOR[1]:
        return True

    return False

def count_streak(board: Board, row: int, col: int, prior: str) -> Tuple[str, int]:
    piece = board[row, col]
    if piece.shape == ShapeConstant.BLANK:
        return None

    # Arah mata angin
    streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    ret_count = (prior, 1)

    # Pergerakan arah mata angin
    for row_ax, col_ax in streak_way:
        mark = 1
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

        if mark > ret_count[1]:
            ret_count = (prior, mark)

        # Apabila ada streak berjumlah 4, langsung return
        if mark == GameConstant.N_COMPONENT_STREAK:
            return (prior, mark)
    
    return ret_count

def countAlmostWin(board: Board, row: int, col: int) -> Tuple[str, int]:
    """
    [DESC]
        Menghitung streak yang akan hampir menang
    [PARAMS]
        state: State -> State game saat ini
        n_player: int -> Nomor giliran pemain
    [RETURN]
        None kalau tidak ada streak yang hampir menang
        Int apabila ada streak yang hampir menang
    """
    piece = board[row, col]

    # Arah mata angin
    streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for prior in GameConstant.WIN_PRIOR:
        mark = 0
        for row_ax, col_ax in streak_way:
            row_ = row + row_ax
            col_ = col + col_ax
            for _ in range(GameConstant.N_COMPONENT_STREAK - 2):
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

            if mark == GameConstant.N_COMPONENT_STREAK - 2 and (not is_out(board, row_, col_)) and board[row_, col_].shape == ShapeConstant.BLANK:
                return (prior, col_)
    
    return None

def almostWin(state: State, n_player: int) -> int:
    """
    [DESC]
        Mengembalikan kolom yang akan hampir menang
    [PARAMS]
        state: State -> State game saat ini
        n_player: int -> Nomor giliran pemain
    [RETURN]
        Jumlah streak piece pada board terbanyak.
        Range dari 0 sampai 4.
    """
    board = state.board
    opponent = state.players[(n_player+1)%2]
    winRow = None
    for row in range(board.row):
        for col in range(board.col):
            # Apabila bentuk bidak sama dengan bentuk pemain, mulai penghitungan streak
            if board[row,col].shape == opponent.shape or board[row,col].color == opponent.color:
                winRow = countAlmostWin(board, row, col)
    
    return winRow

def score(state: State, n_player: int) -> Tuple[str, int]:
    """
    [DESC]
        Fungsi objective function
    [PARAMS]
        state: State -> State game saat ini
        n_player: int -> Nomor giliran pemain
    [RETURN]
        Jumlah streak piece pada board terbanyak.
        Range dari 0 sampai 4.
    """
    board = state.board
    stateScore = ("NONE", 0)
    # Penelusuran seluruh kolom dan baris
    for row in range(board.row):
        for col in range(board.col):
            # Apabila bentuk bidak sama dengan bentuk pemain, mulai penghitungan streak
            if board[row,col].shape == state.players[n_player].shape:
                tempScore = count_streak(board, row, col, GameConstant.WIN_PRIOR[0])
                if scoreGreater(tempScore, stateScore):
                    stateScore = tempScore

            # # Apabila warna bidak sama dengan warna pemain, mulai penghitungan streak
            if board[row,col].color == state.players[n_player].color:
                tempScore = count_streak(board, row, col, GameConstant.WIN_PRIOR[1])
                if scoreGreater(tempScore, stateScore):
                    stateScore = tempScore
                
    return stateScore

class Minimax:
    def __init__(self):
        self.thinking_time = 0
        self.best_movement = None
    
    def getMoves(self, n_player, state: State) -> List[Tuple[str, str]]:
        """
        Menghasilkan list suksesor dari sebuah state board
        """
        moveList = []
        player = state.players[n_player]
        opponent = state.players[(n_player+1)%2]

        for i in range(7):
            if player.quota[player.shape] != 0:
                moveList.append((i, player.shape))

        for i in range(7):
            if player.quota[opponent.shape] != 0:
                moveList.append((i, opponent.shape))

        return moveList

    def minimax(self, n_player: int, state: State, depth: int) -> Tuple[str, str]:
        # Inisialisasi alpha beta
        alpha = (GameConstant.WIN_PRIOR[1], -1000)
        nodeScore = (GameConstant.WIN_PRIOR[1], -1000)
        beta = (GameConstant.WIN_PRIOR[0], 1000)
        # Get move list
        moveList = self.getMoves(n_player, state)

        for move in moveList:
            # Deep copy state and do move
            newState = deepcopy(state)
            valid = place(newState, n_player, move[1], move[0])

            if (valid != -1):
                # Get opponent action
                minValue = self.minABValue(newState, (n_player+1)%2, alpha, beta, depth+1)

                if scoreGreater(minValue, alpha):
                    nodeScore = minValue
                    self.best_movement = move

                alpha = maxScore(nodeScore, alpha)

        return self.best_movement

    def minABValue(self, state: State, n_player: int, alpha: Tuple[str, int], beta: Tuple[str, int], depth: int) -> Tuple[str, int]:
        """
        Cari skor minimum dengan melakukan aksi musuh. Mengembalikan skor.
        """
        nodeScore = (GameConstant.WIN_PRIOR[0], 1000)
        moveList = self.getMoves(n_player, state)

        for move in moveList:
            # Deep copy state and do move
            newState = deepcopy(state)
            valid = place(newState, n_player, move[1], move[0])
            # If placement valid, count nodeScore
            if (valid != -1):
                nodeScore = minScore(nodeScore, self.maxABValue(newState, (n_player+1)%2, alpha, beta, depth+1))
                
                # Prune
                if scoreGreater(alpha, nodeScore):
                    return nodeScore

                beta = minScore(beta, nodeScore)

        return nodeScore

    def maxABValue(self, state: State, n_player: int, alpha: Tuple[str, int], beta: Tuple[str, int], depth: int) -> Tuple[str, int]:
        """
        Cari skor maksimum. Mengembalikan score
        """
        # Apabila node daun, kembalikan score node berdasarkan objective function
        if depth == 2:
            terminalScore = score(state, n_player)
            return terminalScore

        nodeScore = (GameConstant.WIN_PRIOR[1], -1000)
        moveList = self.getMoves(n_player, state)

        for move in moveList:
            # Deep copy state and do move
            newState = deepcopy(state)
            valid = place(newState, n_player, move[1], move[0])

            if (valid != -1):
                nodeScore = maxScore(nodeScore, self.minABValue(newState, (n_player+1)%2, alpha, beta, depth+1))
                #if beta < nodeScore, prune
                if scoreSmaller(beta, nodeScore):
                    return nodeScore
                #update alpha
                alpha = maxScore(alpha, nodeScore)

        return nodeScore

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        if state.round == 1 or state.round == 2:
            return (random.randint(0, 6), state.players[n_player].shape)

        almostWinRow = almostWin(state, n_player)
        if almostWinRow:
            if almostWinRow[0] == GameConstant.SHAPE:
                return (almostWinRow[1], state.players[n_player].shape)
            else:
                return (almostWinRow[1], random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))

        while (time() < self.thinking_time):
            self.minimax(n_player, state, 0)
            break #Break if finished exploring successor tree
        
        return self.best_movement