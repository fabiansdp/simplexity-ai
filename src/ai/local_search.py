import random
import math
from time import time
from typing import Tuple
from copy import deepcopy

from src.constant import ShapeConstant, GameConstant
from src.model import State, Board
from src.utility import place, is_out, check_streak
'''
Langkah menentukan value/nilai
1. cari row dari column dengan fungsi getRow pada utility
2. win priority shape>color
3. waktu berfikir diimplement disini, tapi caranya gimanaaaa
4. local search pake simulated annealing, pake asumsi T=1000 mungkin


Algoritma
1. set max time
2. random
3. hitung nilai
4. kalau lebih baik ambil
5. lebih buruk coba random lalu compare dengan T
6. random ok => ambil return
7. 

best = random
while(self.thinking_time >= time()):
    #body
    #doing SA

    #if ok then best = SA

ret best;
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

class LocalSearch:
    def __init__(self):
        self.state = None
        self.player = None

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        self.state = deepcopy(state)
        self.player = n_player
        #Set Suhu dan pengurangan suhu
        T = 1000
        a = 0.1
        
        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        
        while(self.thinking_time >= time()):
            new_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
            tempState = deepcopy(self.state)

            if(
                not is_out(self.state.board,getRow(self.state, self.player, new_movement[1], int(new_movement[0])),new_movement[0]) 
                and not is_out(self.state.board,getRow(self.state, self.player, best_movement[1], int(best_movement[0])),best_movement[0])
            ):
                place(tempState, self.player, new_movement[1], int(new_movement[0]))
                place(self.state, self.player, best_movement[1], int(best_movement[0]))


                if(score(tempState, self.player) > score(self.state, self.player)):
                    best_movement = new_movement
                else:
                    new_cost = score(tempState, self.player)
                    old_cost = score(self.state, self.player)
                    try:
                        e = math.exp(old_cost - new_cost / T)
                    except OverflowError:
                        e = 1
                    if(e > random.uniform(0,1)):
                        best_movement = new_movement
                
                if(score(tempState, self.player)==4):
                    #auto break jika score sudah maksimal (skor maksimal yang dapat diperoleh adalah 2)
                    break
                else:
                    T -= T*a
                
                self.state = deepcopy(state)
            elif(
                not is_out(self.state.board,getRow(self.state, self.player, new_movement[1], int(new_movement[0])),new_movement[0]) 
                and is_out(self.state.board,getRow(self.state, self.player, best_movement[1], int(best_movement[0])),best_movement[0])
                ):
                best_movement = new_movement


        return best_movement