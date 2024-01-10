from cube import *
from solutionTools import *
from queue import Queue
import json
import copy
    
class GeneratePruningTable:
    def __init__(self):
        pass

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
                    for i in range(6):
                        for j in range(2):
                            newCube = Cube(state=copy.deepcopy(cube.getState()))
                            if j == 0:
                                dir = 1
                            else:
                                dir = -1
                            newCube.rotateFace(i, dir)
                            queue.put(Cube(state=newCube.getState().copy()))
                layer_size -= 1
            print(f"Depth {depth} complete")
            if depth == max_depth:
                break
            depth += 1
        return table
    
    def genG0(self):
        m = Masker()
        masks = Masks()
        g0from, g0to = masks.getG0Mask()
        maskedCube = m.mask(Cube(), g0from, g0to)
        table = self.BFS(maskedCube, max_depth=100)
        print(len(table))
        self.writeTableToFile(table, r"Data\G0.json")
    
    def writeTableToFile(self, table: dict, directory: str):
        with open(directory, "w") as f:
            json.dump(table, f)

g = GeneratePruningTable()

g.genG0()