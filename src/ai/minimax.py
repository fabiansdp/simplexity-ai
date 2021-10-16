import random
from time import time

from src.constant import ShapeConstant, GameConstant
from src.model import State, Board, Piece
from src.utility import is_full, is_out, check_streak, getRow, score

from typing import Tuple, List

'''
Minimax Alpha Beta Pruning
'''
class Minimax:
    def __init__(self):
        self.n_player = 0
        self.board = None
        self.thinking_time = 0
        self.alpha = 1000
        self.beta = -1000
    
    def _score(self, solusi : Tuple[str, str]) -> int:
        #daftar skor
        # -1 ketika is out
        #  0 ketika check streak None
        # 1 ketika check streak mendapat color
        # 2 ketika check streak mendapat shape
        skor = -1
        if self.board == None or self.state == None : return -1
        curr_col = solusi[0]
        curr_row = getRow(self.state, self.n_player, solusi[1], curr_col)

        print(curr_row)
        if is_out(self.board, curr_row, curr_col):
            return -1
        
        cs = check_streak(self.board, curr_row, curr_col)
        skor = 0 if cs == None else (2 if cs[0] == GameConstant.SHAPE else 1)
        
        return skor

    def successors(self) -> List[Tuple[str, str]]:
        """
        Menghasilkan list suksesor dari sebuah state board
        """
        succList = []
        
        for i in range(7):
            succList.append((i, ShapeConstant.CIRCLE))
            succList.append((i, ShapeConstant.CROSS))

        return succList


    def minimax(self, state: State) -> Tuple[str, str]:
        succList = self.successors()

        for succ in succList:
            print(succ, "Score: ", score(succ, state, self.n_player))

        return (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        self.n_player = n_player
        self.state = state
        self.board = state.board
        
        best_movement = self.minimax(state)
            
        return best_movement
