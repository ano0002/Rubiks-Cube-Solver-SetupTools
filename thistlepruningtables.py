from cube import *
from solutionTools import *
from queue import Queue
import json
import copy
    
class GeneratePruningTable:
    m = Masker()
    masks = Masks()
    # All moves
    validMoves = [(0,1,1), (0,-1,1), (0,1,2), (1,1,1), (1,-1,1), (1,1,2), (2,1,1), (2,-1,1), (2,1,2), (3,1,1), (3,-1,1), (3,1,2), (4,1,1), (4,-1,1), (4,1,2), (5,1,1), (5,-1,1), (5,1,2)]
    def __init__(self):
        pass
    
    def setMovesG0(self):
        # All moves
        self.validMoves = [(0,1,1), (0,-1,1), (0,1,2), (1,1,1), (1,-1,1), (1,1,2), (2,1,1), (2,-1,1), (2,1,2), (3,1,1), (3,-1,1), (3,1,2), (4,1,1), (4,-1,1), (4,1,2), (5,1,1), (5,-1,1), (5,1,2)]

    def setMovesG1(self):
        #U, F2, R, B2, L, D
        self.validMoves = [(0,1,1), (0,-1,1), (0,1,2), (1,1,2), (2,1,1), (2,-1,1), (2,1,2), (3,1,2), (4,1,1), (4,-1,1), (4,1,2), (5,1,1), (5,-1,1), (5,1,2)]

    def setMovesG2(self):
        # U, D, F2, B2, R2, L2
        self.validMoves = [(0,1,1), (0,-1,1), (0,1,2), (1,1,2), (2,1,2), (3,1,2), (4,1,2), (5,1,1), (5,-1,1), (5,1,2)]

    def setMovesG3(self):
        # U2, D2, F2, B2, R2, L2
        self.validMoves = [(0,1,2), (1,1,2), (2,1,2), (3,1,2), (4,1,2), (5,1,2)]

    def BFS(self, start: Cube, max_depth: int=8, customStart: list=None) -> dict:
        queue: Queue[Cube] = Queue()
        depth = 0
        table = {}
        if customStart is None:
            queue.put(start)
        else:
            for cube in customStart:
                queue.put(cube)
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
    
    def CornerBFS(self, start: Cube, max_depth: int=8) -> list:
        queue: Queue[Cube] = Queue()
        depth = 0
        stateList = []
        queue.put(start)
        cube: Cube = None
        while queue.qsize() > 0:
            layer_size = queue.qsize()
            while layer_size > 0:
                cube = queue.get()
                if cube.getState() not in stateList:
                    stateList.append(cube.getState())
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
        return stateList
    
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
    
    def genG2CornerPermutations(self):
        self.setMovesG3()
        cube = Cube()
        mask, maskTo = self.masks.getG2CornerMask()
        maskedCube = self.m.mask(cube, mask, maskTo)
        list = self.CornerBFS(maskedCube, max_depth=8)
        print(len(list))
        self.writeListToFile(list, r"Data\G2Corners.json")

    def genG2(self):
        self.setMovesG2()
        with open(r"Data\G2Corners.json", "r") as f:
            stateList: list = json.load(f)
        cubeList = []
        for state in stateList:
            cubeList.append(Cube(state=state))
        table = self.BFS(None, 7, customStart=cubeList)
        print(len(table))
        self.writeTableToFile(table, r"Data\G2.json")

    def writeListToFile(self, list: list, directory: str):
        with open(directory, "w") as f:
            json.dump(list, f)

    def writeTableToFile(self, table: dict, directory: str):
        with open(directory, "w") as f:
            json.dump(table, f)
    

g = GeneratePruningTable()
g.genG2()
