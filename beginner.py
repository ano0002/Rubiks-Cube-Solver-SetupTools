from cube import *
import queue
import json

class BeginnerSolver:
    def __init__(self, cube: Cube):
        self.cube = cube
        self.phase = 0
        with open("edgecoords.json", "r") as f:
            self.edgeCoordsDict = json.load(f)
            
    def getTargetCoordEdge(self, coords: tuple) -> tuple:
        # Up right down left
        coordslist = [(0,1), (1,2), (2,1), (1,0)]
        edge = coordslist.index((coords[1],coords[2]))
        
        if 1 <= coords[0] <= 4 and edge in [1, 3]:
            adjEdge = (edge + 2) % 4
            if edge == 1:
                adjFace = (coords[0] - 1) % 4
            else:
                adjFace = (coords[0] + 1) % 4
        elif 1 <= coords[0] <= 4 and edge in [0, 2]:
            if edge == 0:
                adjFace = 0
                if coords[0] == 1:
                    adjEdge = 2
                elif coords[0] == 2:
                    adjEdge = 1
                elif coords[0] == 3:
                    adjEdge = 0
                else:
                    adjEdge = 3
            else:
                adjFace = 5
                adjEdge = coords[0] - 1
        elif coords[0] == 0:
            adjEdge = 0
            if edge == 0:
                adjFace = 3
            elif edge == 1:
                adjFace = 2
            elif edge == 2:
                adjFace = 1
            else:
                adjFace = 4
        elif coords[0] == 5:
            adjEdge = 2
            adjFace = edge + 1

        adjCoords = coordslist[adjEdge]
        adjCol = self.cube.getState()[adjFace][adjCoords[0]][adjCoords[1]]
        col = self.cube.getState()[coords[0]][coords[1]][coords[2]]
        key = str(col) + str(adjCol)
        target = self.edgeCoordsDict[key]
        return (int(target[0]), int(target[1]), int(target[2]))

    def whiteCross(self): # Phase 0
        whiteEdgeCoords = queue.Queue()
        cubeState = self.cube.getState()
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    if abs(j-k) == 1:
                        if cubeState[i][j][k] == 0:
                            whiteEdgeCoords.put((i,j,k))
        
        while not whiteEdgeCoords.empty():
            print(self.getTargetCoordEdge(whiteEdgeCoords.get()))

c = getRandomScramble(1)
b = BeginnerSolver(c)

b.whiteCross()
