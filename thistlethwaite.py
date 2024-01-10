from cube import *
import json
from solutionTools import *

class Thistlethwaite:
    validMoves = [(0,1,1), (0,-1,1), (1,1,1), (1,-1,1), (2,1,1), (2,-1,1), (3,1,1), (3,-1,1), (4,1,1), (4,-1,1), (5,1,1), (5,-1,1)]
    solver = SolverTools()
    def __init__(self):
        pass

    def DFS(self, cube: Cube, solution: str, depthRemaining: int, table: dict, tableMaxDepth: int) -> str:
        if self.solver.isSolved(cube):
            return solution.strip()
        
        try:
            lowerbound = table[cube.generateKey()]
        except:
            lowerbound = tableMaxDepth + 1
        
        if lowerbound > depthRemaining:
            return None

        for move in self.validMoves:
            for i in range(move[2]):
                cube.rotateFace(move[0], move[1])
            result = self.DFS(cube, solution + " " + str(move), depthRemaining-1)
            for i in range(move[2]):
                cube.rotateFace(move[0], -move[1])
            if result is not None:
                return result
        return None
    
    def IDDFS(self, cube: Cube, table: dict, tableMaxDepth:int, max_depth: int=5) -> str:
        for depth in range(max_depth):
            solution = self.DFS(cube, "", depth + 1, table, tableMaxDepth)
            if solution is not None:
                return solution
        else:
            return None


cube = getRandomScramble(5)

t = Thistlethwaite()


