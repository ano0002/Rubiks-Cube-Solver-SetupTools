from cube import *
from solutionTools import *
from queue import Queue
import json

class Masker:
    def __init__(self):
        pass

    def mask(self, cube: Cube, mask: list, maskTo: list, defaultMask: str="X") -> Cube:
        ifCube = ifCubeGen(cube).constructIFCube().getState()
        outCube = Cube().getState()
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    if ifCube[i][j][k] in mask:
                        outCube[i][j][k] = maskTo[mask.index(ifCube[i][j][k])]
                    else:
                        outCube[i][j][k] = defaultMask
        
        return Cube(state=outCube)
    
class GeneratePruningTable:
    def __init__(self):
        pass

    def BFS(self, start: Cube) -> dict:
        queue: Queue[Cube] = Queue()
        depth = 0
        table = {}
        queue.put(start)
        while queue.qsize() > 0:
            layer_size = queue.qsize()
            while layer_size > 0:
                cube = queue.get()
                key = cube.generateKey()
                if key not in table:
                    table[key] = depth
                    for i in range(6):
                        for j in range(2):
                            newCube = Cube(state=list(cube.getState()))
                            if j == 0:
                                dir = 1
                            else:
                                dir = -1
                            newCube.rotateFace(i, dir)
                            queue.put(Cube(state=newCube.getState().copy()))
                layer_size -= 1
            print(f"Depth {depth} complete")
            depth += 1
        return table
    
    def writeTableToFile(self, table: dict, directory: str):
        with open(directory, "w") as f:
            json.dump(table, f)

cube = Cube()

mask = ["U0"]
maskTo = ["U"]

m = Masker()
masked = m.mask(cube, mask, maskTo)
#masked.rotateFace(4, 1)

#print(masked.generateKey())

gen = GeneratePruningTable()

table = gen.BFS(masked)
gen.writeTableToFile(table, r"testDB.json")