import random
import math
from time import time

from src.constant import ShapeConstant
from src.model import State
from src.constant import GameConstant
from typing import Tuple, List
from src.utility import is_full, is_out, check_streak, place
'''
Langkah menentukan value/nilai
1. cari row dari column dengan fungsi place pada utility
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

class LocalSearch:
    def __init__(self):
        self.board = None
        self.state = None
        self.player = None

    def _score(self, solusi : Tuple[str, str]) -> int:
        #daftar skor
        # -1 ketika is out
        #  0 ketika check streak None
        # 1 ketika check streak mendapat color
        # 2 ketika check streak mendapat shape
        skor = -1
        if self.board == None or self.state == None : return -1
        curr_col = solusi[0]
        curr_row = place(self.state, self.player, solusi[1], str(curr_col))

        if is_out(self.board, curr_row, curr_col):
            return -1
        
        cs = check_streak(self.board, curr_row, curr_col)
        skor = 0 if cs == None else (2 if cs[0] == GameConstant.SHAPE else 1)
        
        return skor

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        self.board = state.board
        self.state = state
        self.player = n_player
        #Set Suhu dan pengurangan suhu
        T = 1000
        a = 0.1
        
        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        while(self.thinking_time >= time()):
            new_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))

            if(self._score(new_movement) > self._score(best_movement)):
                best_movement = new_movement
            else:
                new_cost = self._score(new_movement)
                old_cost = self._score(best_movement)
                try:
                    e = math.exp(old_cost - new_cost / T)
                except OverflowError:
                    e = 1
                if(e > random.uniform(0,1)):
                    best_movement = new_movement
            
            if(self._score(best_movement)==2):
                #auto break jika score sudah maksimal (skor maksimal yang dapat diperoleh adalah 2)
                break
            else:
                T -= T*a

        return best_movement