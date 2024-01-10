from cube import *
from solutionTools import *

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
    
cube = Cube()

mask = ["F1", "B4"]
maskTo = ["RED", "BACK"]

m = Masker()
print(m.mask(cube, mask, maskTo).getState())