from cube import *
import json
from solutionTools import *

class Thistlethwaite:
    # All moves
    validMoves = [(0,1,1), (0,-1,1), (0,1,2), (1,1,1), (1,-1,1), (1,1,2), (2,1,1), (2,-1,1), (2,1,2), (3,1,1), (3,-1,1), (3,1,2), (4,1,1), (4,-1,1), (4,1,2), (5,1,1), (5,-1,1), (5,1,2)]
    solver = SolverTools()
    masker = Masker()
    maskDB = Masks()

    def __init__(self):
        pass

    def G0Mask(self, cube: Cube) -> Cube:
        mask, maskTo = self.maskDB.getG0Mask()
        return self.masker.mask(cube, mask, maskTo)
    
    def G1Mask(self, cube: Cube) -> Cube:
        mask, maskTo = self.maskDB.getG1Mask()
        return self.masker.mask(cube, mask, maskTo)

    def setMovesG0(self):
        # All moves
        self.validMoves = [(0,1,1), (0,-1,1), (0,1,2), (1,1,1), (1,-1,1), (1,1,2), (2,1,1), (2,-1,1), (2,1,2), (3,1,1), (3,-1,1), (3,1,2), (4,1,1), (4,-1,1), (4,1,2), (5,1,1), (5,-1,1), (5,1,2)]

    def setMovesG1(self):
        #U, F2, R, B2, L, D
        self.validMoves = [(0,1,1), (0,-1,1), (0,1,2), (1,1,2), (2,1,1), (2,-1,1), (2,1,2), (3,1,2), (4,1,1), (4,-1,1), (4,1,2), (5,1,1), (5,-1,1), (5,1,2)]

    def startG0(self, cube: Cube):
        self.setMovesG0()
        with open(r"Data\G0.json", "r") as f:
            self.g0Table = json.load(f)
        maskedCube = self.G0Mask(cube)
        print(self.IDDFS(maskedCube, self.g0Table, 7, 10))
    
    def startG1(self):
        self.setMovesG1()
        with open(r"Data\G1.json", "r") as f:
            self.g1Table = json.load(f)

    def DFS(self, cube: Cube, solution: str, depthRemaining: int, table: dict, tableMaxDepth: int) -> str:
        if self.solver.isSolved(cube):
            return solution.strip()
        
        try:
            lowerbound = table[cube.generateKey()]
        except:
            lowerbound = tableMaxDepth + 1
        
        if lowerbound == 0:
            return solution
        if lowerbound > depthRemaining:
            return None

        for move in self.validMoves:
            for i in range(move[2]):
                cube.rotateFace(move[0], move[1])
            result = self.DFS(cube, solution + " " + str(move), depthRemaining-1, table, tableMaxDepth)
            for i in range(move[2]):
                cube.rotateFace(move[0], -move[1])
            if result is not None:
                return result
        return None
    
    def IDDFS(self, cube: Cube, table: dict, tableMaxDepth:int, max_depth: int=10) -> str:
        for depth in range(max_depth):
            solution = self.DFS(cube, "", depth + 1, table, tableMaxDepth)
            if solution is not None:
                return solution
        else:
            return None


cube = getRandomScramble(100)

t = Thistlethwaite()

t.startG0(cube)
