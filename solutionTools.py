from cube import *
import json

class Masker:
    def __init__(self):
        pass

    def mask(self, cube: Cube, mask: list, maskTo: list, defaultMask: str="X") -> Cube:
        ifCube = ICubeGen(cube).constructICube().getState()
        outCube = Cube().getState()
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    if ifCube[i][j][k] in mask:
                        outCube[i][j][k] = maskTo[mask.index(ifCube[i][j][k])]
                    else:
                        outCube[i][j][k] = defaultMask
        
        return Cube(state=outCube)

class ICubeGen:
    mappings = {
        0 : "U",
        1 : "F",
        2 : "R",
        3 : "B",
        4 : "L",
        5 : "D"
    }

    def __init__(self, cube: Cube):
        self.cube = cube
        with open(r"Data\edgecoords.json", "r") as f:
            self.edgeCoordsDict = json.load(f)
        
        with open(r"Data\cornercoords.json", "r") as f:
            self.cornerCoordsDict = json.load(f)
    
    def constructICube(self) -> Cube:
        ifcubearray = Cube().getState()
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    if abs(j-k) == 1:
                        ifcubearray[i][j][k] = self.getIEdge((i,j,k))
                    elif j == k == 1:
                        ifcubearray[i][1][1] = self.mappings[i] + "4"
                    else:
                        ifcubearray[i][j][k] = self.getICorner((i,j,k))
        ifCube = Cube(state=ifcubearray)

        return ifCube


    def getIEdge(self, coords: tuple) -> str:
        # Up right down left
        coordslist = [(0,1), (1,2), (2,1), (1,0)]
        edge = coordslist.index((coords[1],coords[2]))
        
        # Get colour of adjacent face
        if 1 <= coords[0] <= 4 and edge in [1, 3]:
            adjEdge = (edge + 2) % 4
            if edge == 3:
                adjFace = (coords[0] - 2) % 4 + 1
            else:
                adjFace = coords[0] % 4 + 1
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

        # Using colour of 2 adjacent faces, find the solved position of the facelet
        key = str(col) + str(adjCol)
        target = self.edgeCoordsDict[key]
        return self.mappings[int(target[0])] + str(3*int(target[1])+int(target[2]))
    
    def getICorner(self, coords: tuple) -> tuple:
        coordsList = [(0,0), (0,2), (2,0), (2,2)]
        corner = coordsList.index((coords[1],coords[2])) # 0 is topleft, 1 is top right, 2 is bottom left, 3 is bottom right

        adjCols = []
        # Find adjacent face colours
        if 1 <= coords[0] <= 4 and corner in [0, 2]:
            adjCorner = corner + 1
            adjFace = (coords[0] - 2) % 4 + 1
            adjCols.append(self.cube.getState()[adjFace][coordsList[adjCorner][0]][coordsList[adjCorner][1]])
            if corner == 0:
                adjFace = 0
                adjCorner = [2, 3, 1, 0][coords[0]-1]
            elif corner == 2:
                adjFace = 5
                adjCorner = [0, 1, 3, 2][coords[0]-1]
            adjCols.append(self.cube.getState()[adjFace][coordsList[adjCorner][0]][coordsList[adjCorner][1]])    
        elif 1 <= coords[0] <= 4 and corner in [1, 3]:
            adjCorner = corner - 1
            adjFace = coords[0] % 4 + 1
            adjCols.append(self.cube.getState()[adjFace][coordsList[adjCorner][0]][coordsList[adjCorner][1]])
            if corner == 1:
                adjFace = 0
                adjCorner = [3, 1, 0, 2][coords[0]-1]
            elif corner == 3:
                adjFace = 5
                adjCorner = [1, 3, 2, 0][coords[0]-1]
            adjCols.append(self.cube.getState()[adjFace][coordsList[adjCorner][0]][coordsList[adjCorner][1]])
        elif coords[0] == 0:
            if corner in [0, 2]:
                adjFace = 4
                adjCorner = corner//2
            else:
                adjFace = 2
                adjCorner = (corner//2 + 1) % 2
            adjCols.append(self.cube.getState()[adjFace][coordsList[adjCorner][0]][coordsList[adjCorner][1]])

            if corner in [0, 1]:
                adjFace = 3
                adjCorner = (corner + 1) % 2
            else:
                adjFace = 1
                adjCorner = corner - 2
            adjCols.append(self.cube.getState()[adjFace][coordsList[adjCorner][0]][coordsList[adjCorner][1]])
        else:
            if corner in [0, 2]:
                adjFace = 4
                if corner == 0:
                    adjCorner = 3
                else:
                    adjCorner = 2
            elif corner in [1, 3]:
                adjFace = 2
                if corner == 1:
                    adjCorner = 2
                else:
                    adjCorner = 3
            adjCols.append(self.cube.getState()[adjFace][coordsList[adjCorner][0]][coordsList[adjCorner][1]])

            if corner in [0, 1]:
                adjFace = 1
                adjCorner = corner + 2
            else:
                adjFace = 3
                adjCorner = (corner - 3) % 2 + 2
            adjCols.append(self.cube.getState()[adjFace][coordsList[adjCorner][0]][coordsList[adjCorner][1]])


        adjCols.sort()
        col = self.cube.getState()[coords[0]][coords[1]][coords[2]]
        key = str(col) + str(adjCols[0]) + str(adjCols[1])
        target = self.cornerCoordsDict[key]
        return self.mappings[int(target[0])] + str(3*int(target[1])+int(target[2]))
    
class SolverTools:
    solvedCube = Cube()
    def __init__(self):
        pass
        
    def isSolved(self, cube: Cube) -> bool:
        return self.solvedCube.getState() == cube.getState()
  
class Masks:
    def __init__(self):
        pass
    
    def getG0Mask(self) -> list:
        mask = ["U1", "U3", "U5", "U7", "F3", "F5", "B3", "B5",  "D1", "D3", "D5", "D7"]
        maskTo = ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]

        return mask, maskTo
    
    def getG1Mask(self) -> list:
        mask = ["U0", "U1", "U2", "U3", "U5", "U6", "U7", "U8", "F3", "F5", "B3", "B5", "D0", "D1", "D2", "D3", "D5", "D6", "D7", "D8"]
        maskTo = ["O", "O", "O", "O", "O", "O", "O", "O", "P", "P", "P", "P", "O", "O", "O", "O", "O", "O", "O", "O"]

        return mask, maskTo
    
    def getG2CornerMask(self) -> list:
        mask = ["U0", "U2", "U6", "U8", "F0", "F2", "F6", "F8", "R0", "R2", "R6", "R8", "B0", "B2", "B6", "B8", "L0", "L2", "L6", "L8", "D0", "D2", "D6", "D8"]
        maskTo = ["U", "U", "U", "U", "F", "F", "F", "F", "R", "R", "R", "R", "B", "B", "B", "B", "L", "L", "L", "L", "D", "D", "D", "D"]

        return mask, maskTo
    
    def getG2Mask(self) -> list:
        mask = ["U0", "U2", "U6", "U8", "F0", "F2", "F6", "F8", "R0", "R2", "R6", "R8", "B0", "B2", "B6", "B8", "L0", "L2", "L6", "L8", "D0", "D2", "D6", "D8", "U1", "U3", "U5", "U7", "F1", "F3", "F5", "F7", "R1", "R3", "R5", "R7", "B1", "B3", "B5", "B7", "L1", "L3", "L5", "L7", "D1", "D3", "D5", "D7"]
        maskTo = ["U", "U", "U", "U", "F", "F", "F", "F", "R", "R", "R", "R", "B", "B", "B", "B", "L", "L", "L", "L", "D", "D", "D", "D", "U", "U", "U", "U", "F", "F", "F", "F", "R", "R", "R", "R", "F", "F", "F", "F", "R", "R", "R", "R", "U", "U", "U", "U"]

        return mask, maskTo