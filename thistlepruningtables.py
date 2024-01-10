from cube import *
from solutionTools import *
from queue import Queue
import json
import copy
    
class GeneratePruningTable:
    m = Masker()
    masks = Masks()
    # All moves
    validMoves = [(0,1,1), (0,-1,1), (1,1,1), (1,-1,1), (2,1,1), (2,-1,1), (3,1,1), (3,-1,1), (4,1,1), (4,-1,1), (5,1,1), (5,-1,1)]
    def __init__(self):
        pass
    
    def setMovesG0(self):
        # All moves
        self.validMoves = [(0,1,1), (0,-1,1), (1,1,1), (1,-1,1), (2,1,1), (2,-1,1), (3,1,1), (3,-1,1), (4,1,1), (4,-1,1), (5,1,1), (5,-1,1)]

    def setMovesG1(self):
        #U, F2, R, B2, L, D
        # Also must now include U2 etc. as not entire tree searched
        self.validMoves = [(0,1,1), (0,-1,1), (0,1,2), (1,1,2), (2,1,1), (2,-1,1), (2,1,2), (3,1,2), (4,1,1), (4,-1,1), (4,1,2), (5,1,1), (5,-1,1), (5,1,2)]

    def BFS(self, start: Cube, max_depth: int=8) -> dict:
        queue: Queue[Cube] = Queue()
        depth = 0
        table = {}
        queue.put(start)
        cube: Cube = None
        while queue.qsize() > 0:
            layer_size = queue.qsize()
            while layer_size > 0:
                cube = queue.get()
                key = cube.generateKey()
                if key not in table:
                    table[key] = depth
                    for move in self.validMoves:
                        newCube = Cube(state=copy.deepcopy(cube.getState()))
                        for i in range(move[2]):
                            newCube.rotateFace(move[0], move[1])
                        queue.put(Cube(state=newCube.getState().copy()))
                layer_size -= 1
            print(f"Depth {depth} complete")
            if depth == max_depth:
                break
            depth += 1
        return table
    
    def genG0(self):
        self.setMovesG0()
        g0from, g0to = self.masks.getG0Mask()
        maskedCube = self.m.mask(Cube(), g0from, g0to)
        table = self.BFS(maskedCube, max_depth=100)
        print(len(table))
        self.writeTableToFile(table, r"Data\G0.json")
    
    def genG1(self):
        self.setMovesG1()
        g1from, g1to = self.masks.getG1Mask()
        maskedCube = self.m.mask(Cube(), g1from, g1to)
        table = self.BFS(maskedCube, max_depth=7)
        print(len(table))
        self.writeTableToFile(table, r"Data\G1.json")
    
    def writeTableToFile(self, table: dict, directory: str):
        with open(directory, "w") as f:
            json.dump(table, f)

