import numpy as np
import random
import time
import sys
import os 
from BaseAI import BaseAI
from Grid import Grid

# TO BE IMPLEMENTED
# 
class PlayerAI(BaseAI):

    def __init__(self) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = None
        self.player_num = None
    
    def getPosition(self):
        return self.pos

    def setPosition(self, new_position):
        self.pos = new_position 

    def getPlayerNum(self):
        return self.player_num

    def getOppPlayerNum(self):
        return 3 - self.player_num

    def setPlayerNum(self, num):
        self.player_num = num

    def eval(self, grid: Grid):
        my_neighbors = grid.get_neighbors(grid.find(self.player_num), True)
        opponent_neighbors = grid.get_neighbors(grid.find(self.getOppPlayerNum()), True)

        return len(my_neighbors) - len(opponent_neighbors)

    def move_minimize(self, grid: Grid, a, b, depth):
        traps = grid.get_neighbors(grid.find(self.getPlayerNum()), True)

        if len(traps) == 0 or depth == 5:
            return None, self.eval(grid)

        next_trap = None
        min_utility = +10000000

        for trap in traps:
            child = grid.clone().trap(trap)
            x, utility = self.move_maximize(child, a, b, depth+1)

            if utility < min_utility:
                next_trap = trap
                min_utility = utility

            if min_utility <= a:
                break

            if min_utility < b:
                b = min_utility

        return (next_trap, min_utility)

    def move_maximize(self, grid: Grid, a, b, depth):
        neighbors = grid.get_neighbors(self.pos, True)

        if len(neighbors) == 0 or depth == 5:
            return None, self.eval(grid)

        next_pos = None
        max_utility = -1000000

        for neighbor in neighbors:
            child = grid.clone().move(neighbor, self.player_num)
            x, utility = self.move_minimize(child, a, b, depth+1)

            if utility > max_utility:
                next_pos = neighbor
                max_utility = utility

            if max_utility >= b:
                break

            if max_utility > a:
                a = max_utility

        return (next_pos, utility)

    def getMove(self, grid: Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player moves.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Trap* actions, 
        taking into account the probabilities of them landing in the positions you believe they'd throw to.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """

        next_pos, utility =  self.move_maximize(grid, -1000000, 1000000, 1)

        return next_pos

    def trap_minimize(self, grid: Grid, a, b, depth):
        neighbors = grid.get_neighbors(grid.find(self.getOppPlayerNum()), True)

        if len(neighbors) == 0 or depth == 5:
            return None, self.eval(grid)

        next_move, min_utility = None, +1000000

        for neighbor in neighbors:
            child = grid.clone().move(neighbor, self.getOppPlayerNum())
            x, utility = self.trap_maximize(grid, a, b, depth+1)

            if utility < min_utility:
                next_move, min_utility = neighbor, utility

            if min_utility <= a:
                break

            if min_utility < b:
                b = min_utility

        return (next_move, min_utility)


    def trap_maximize(self, grid: Grid, a, b, depth):
        neighbors = grid.get_neighbors(grid.find(self.getOppPlayerNum()), True)

        if len(neighbors) == 0 or depth == 5:
            return None, self.eval(grid)

        next_trap, max_utility = None, -1000000

        for neighbor in neighbors:
            child = grid.clone().trap(neighbor)
            x, utility = self.trap_minimize(child, a, b, depth+1)

            if utility > max_utility:
                next_trap = neighbor
                max_utility = utility

            if max_utility >= b:
                break

            if max_utility > a:
                a = max_utility

        return (next_trap, max_utility)

    def getTrap(self, grid : Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.
        
        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions, 
        taking into account the probabilities of it landing in the positions you want. 
        
        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """

        next_trap, utility = self.trap_maximize(grid, -1000000, 1000000, 1)

        return next_trap
        

    