import random
from time import time
from typing import Tuple, List
from copy import deepcopy

from src.constant import ShapeConstant
from src.model import Board, State, Piece
from src.utility import getRow, score, place

'''
Minimax Alpha Beta Pruning
'''
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
        Cari skor maksimum.
        """
        # Apabila node daun, kembalikan score node berdasarkan objective function
        if depth == 2:
            return random.choice([-1, 0, 1, 2])

        nodeScore = -1000
        moveList = self.getMoves(n_player, state)

        for move in moveList:
            # Deep copy state and do move
            newState = deepcopy(state)
            valid = place(newState, n_player, move[1], move[0])

            if (valid != -1):
                nodeScore = max(nodeScore, self.minABValue(newState, (n_player+1)%2), alpha, beta, depth+1)
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
            break
            
        return self.best_movement
