import random
import math
from time import time

from src.constant import ShapeConstant
from src.model import State
from typing import Tuple
from src.utility import place, score, is_out, getRow
from copy import deepcopy
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