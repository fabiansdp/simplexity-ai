import random
import math
from time import time

from src.constant import ShapeConstant
from src.model import State
from typing import Tuple
from src.utility import score
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

class LocalSearch:
    def __init__(self):
        self.board = None
        self.state = None
        self.player = None

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        self.board = state.board
        self.state = state
        self.player = n_player
        #Set Suhu dan pengurangan suhu
        T = 1000
        a = 0.1
        
        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))

        while(self.thinking_time >= time()):
            new_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))

            if(score(new_movement, self.state, self.player) > score(best_movement, self.state, self.player)):
                best_movement = new_movement
            else:
                new_cost = score(new_movement, self.state, self.player)
                old_cost = score(best_movement, self.state, self.player)
                try:
                    e = math.exp(old_cost - new_cost / T)
                except OverflowError:
                    e = 1
                if(e > random.uniform(0,1)):
                    best_movement = new_movement
            
            if(score(best_movement, self.state, self.player)==2):
                #auto break jika score sudah maksimal (skor maksimal yang dapat diperoleh adalah 2)
                break
            else:
                T -= T*a

        return best_movement