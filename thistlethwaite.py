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

    def G0(self, cube: Cube) -> Cube:
        self.setMovesG0()
        with open(r"Data\G0.json", "r") as f:
            g0Table = json.load(f)
        maskedCube = self.G0Mask(cube)
        solution = self.IDDFS(maskedCube, g0Table, 7, 10)
        for move in solution:
            for i in range(move[2]):
                cube.rotateFace(move[0], move[1])
        return cube
    
    def G1(self, cube: Cube) -> Cube:
        self.setMovesG1()
        with open(r"Data\G1.json", "r") as f:
            g1Table = json.load(f)
        maskedCube = self.G1Mask(cube)
        solution = self.IDDFS(maskedCube, g1Table, 7, 10)
        for move in solution:
            for i in range(move[2]):
                cube.rotateFace(move[0], move[1])
        return cube

    def DFS(self, cube: Cube, solution: list, depthRemaining: int, table: dict, tableMaxDepth: int) -> str:
        if self.solver.isSolved(cube):
            return solution
        
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
            extSolution = solution.copy()
            extSolution.append(move)
            result = self.DFS(cube, extSolution, depthRemaining-1, table, tableMaxDepth)
            for i in range(move[2]):
                cube.rotateFace(move[0], -move[1])
            if result is not None:
                return result
        return None
    
    def IDDFS(self, cube: Cube, table: dict, tableMaxDepth:int, max_depth: int=10) -> str:
        for depth in range(max_depth):
            solution = self.DFS(cube, [], depth + 1, table, tableMaxDepth)
            if solution is not None:
                return solution
        else:
            return None


cube = getRandomScramble(100)

t = Thistlethwaite()

cube = t.G0(cube)

cube = t.G1(cube)

