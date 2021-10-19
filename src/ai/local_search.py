import random
import math
from time import time
from typing import Tuple
from copy import deepcopy

from src.constant import ShapeConstant, GameConstant
from src.model import State, Board
from src.utility import place, is_out
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

class LocalSearch:
    def __init__(self):
        self.state = None
        self.player = None

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + (thinking_time * 0.999)
        self.state = deepcopy(state)
        self.player = n_player
        #Set Suhu dan pengurangan suhu
        T = 1000
        a = 0.1
        
        #melakukan random solusi awal
        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        
        while(self.thinking_time > time()):
            #melakukan random solusi baru
            new_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
            tempState = deepcopy(self.state)

            #cek apakah solusi yang dihasilkan out of board tidak
            if(
                not is_out(self.state.board,getRow(self.state, self.player, new_movement[1], int(new_movement[0])),new_movement[0]) 
                and not is_out(self.state.board,getRow(self.state, self.player, best_movement[1], int(best_movement[0])),best_movement[0])
            ):
                place(tempState, self.player, new_movement[1], int(new_movement[0]))
                place(self.state, self.player, best_movement[1], int(best_movement[0]))

                #cek apakah solusi baru punya obj score lebih baik
                if(score(tempState, self.player) > score(self.state, self.player)):
                    best_movement = new_movement
                else:
                    new_cost = score(tempState, self.player)
                    old_cost = score(self.state, self.player)
                    #mencoba untuk  melakukan penerimaan solusi lebih buruk jika random(0,1) < e^(ΔE/T)
                    try:
                        e = math.exp(old_cost - new_cost / T)
                    except OverflowError:
                        e = 1
                    if(e > random.uniform(0,1)):
                        best_movement = new_movement
                
                #karena skor maks adalah 4, jika sudah mencapai 4 maka terminate saja dan bakal return solusi
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