import random
from time import time

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List
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

class Minimax:
    def __init__(self):
        pass
    
    def MinMax(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return best_movement
