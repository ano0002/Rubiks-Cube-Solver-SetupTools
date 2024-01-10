from cube import *
import json
from solutionTools import *

class Thistlethwaite:
    validMoves = [(0,1,1), (0,-1,1), (1,1,1), (1,-1,1), (2,1,1), (2,-1,1), (3,1,1), (3,-1,1), (4,1,1), (4,-1,1), (5,1,1), (5,-1,1)]
    solver = SolverTools()
    def __init__(self):
        pass

    def genMaskedCube(self, cube: Cube, mask: list) -> Cube:
        pass

    def DFS(self, cube: Cube, solution: str, depthRemaining: int) -> str:
        if self.solver.isSolved(cube):
            return solution.strip()
        if depthRemaining == 0:
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
    
    def IDDFS(self, cube: Cube, max_depth=5):
        for depth in range(max_depth):
            solution = self.DFS(cube, "", depth + 1)
            if solution is not None:
                return solution
        else:
            return None


cube = getRandomScramble(5)

t = Thistlethwaite()

print(t.IDDFS(cube, 5))

