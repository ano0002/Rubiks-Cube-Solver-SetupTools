import random

class Cube:
    def __init__(self, state:list=None) -> None:
        if state == None:
            self.cube = [[[0,0,0],[0,0,0],[0,0,0]],[[1,1,1],[1,1,1],[1,1,1]],
                         [[2,2,2],[2,2,2],[2,2,2]],[[3,3,3],[3,3,3],[3,3,3]], 
                         [[4,4,4],[4,4,4],[4,4,4]],[[5,5,5],[5,5,5],[5,5,5]]]
        #WRBOGY
        #012345
        # Each 2d array is the colours of a face, rather than the cubepieces.
        else:
            self.cube = state
    
    def __str__(self) -> str:
        return str(self.cube)

    def getState(self) -> list:
        return self.cube

    def getCornerCode(self) -> str:
        out = ""
        for i in range(6):
            out += str(self.cube[i][0][0]) + str(self.cube[i][0][2]) + str(self.cube[i][2][0]) + str(self.cube[i][2][2])
        return out

    def rotateFace(self, face: int, dir: int) -> None:
        if dir == 1: # 1 is anticlockwise, -1 is clockwise
            self.cube[face] = list(list(x) for x in zip(*self.cube[face]))[::-1]
        elif dir == -1:
            self.cube[face] = list(list(x) for x in zip(*self.cube[face][::-1]))

        if dir == 1:
            if face == 0:
                self.cube[1][0], self.cube[2][0], self.cube[3][0], self.cube[4][0] = (self.cube[4][0],
                                                                                    self.cube[1][0],
                                                                                    self.cube[2][0],
                                                                                    self.cube[3][0]
                                                                                    )
            elif face == 5:
                self.cube[1][2], self.cube[2][2], self.cube[3][2], self.cube[4][2] = (self.cube[2][2], 
                                                                                      self.cube[3][2], 
                                                                                      self.cube[4][2],
                                                                                      self.cube[1][2])
                                                                                    
            elif face == 1:
                self.cube[0][2][0], self.cube[0][2][1], self.cube[0][2][2], self.cube[2][0][0], self.cube[2][1][0], self.cube[2][2][0], self.cube[5][0][2], self.cube[5][0][1], self.cube[5][0][0], self.cube[4][2][2], self.cube[4][1][2], self.cube[4][0][2] = (self.cube[2][0][0], self.cube[2][1][0], self.cube[2][2][0],
                                                                                                                                                                                                                                                                self.cube[5][0][2], self.cube[5][0][1], self.cube[5][0][0],
                                                                                                                                                                                                                                                                self.cube[4][2][2], self.cube[4][1][2], self.cube[4][0][2],
                                                                                                                                                                                                                                                                self.cube[0][2][0], self.cube[0][2][1], self.cube[0][2][2])
            
            elif face == 3:
                self.cube[0][0][2], self.cube[0][0][1], self.cube[0][0][0], self.cube[4][0][0], self.cube[4][1][0], self.cube[4][2][0], self.cube[5][2][0], self.cube[5][2][1], self.cube[5][2][2], self.cube[2][2][2], self.cube[2][1][2], self.cube[2][0][2] = (self.cube[4][0][0], self.cube[4][1][0], self.cube[4][2][0],
                                                                                                                                                                                                                                                                self.cube[5][2][0], self.cube[5][2][1], self.cube[5][2][2],
                                                                                                                                                                                                                                                                self.cube[2][2][2], self.cube[2][1][2], self.cube[2][0][2],
                                                                                                                                                                                                                                                                self.cube[0][0][2], self.cube[0][0][1], self.cube[0][0][0])
            elif face == 2:
                self.cube[0][2][2], self.cube[0][1][2], self.cube[0][0][2], self.cube[3][0][0], self.cube[3][1][0], self.cube[3][2][0], self.cube[5][2][2], self.cube[5][1][2], self.cube[5][0][2], self.cube[1][2][2], self.cube[1][1][2], self.cube[1][0][2] = (self.cube[3][0][0], self.cube[3][1][0], self.cube[3][2][0],
                                                                                                                                                                                                                                                                self.cube[5][2][2], self.cube[5][1][2], self.cube[5][0][2],
                                                                                                                                                                                                                                                                self.cube[1][2][2], self.cube[1][1][2], self.cube[1][0][2],
                                                                                                                                                                                                                                                                self.cube[0][2][2], self.cube[0][1][2], self.cube[0][0][2])
            elif face == 4:
                self.cube[0][0][0], self.cube[0][1][0], self.cube[0][2][0], self.cube[1][0][0], self.cube[1][1][0], self.cube[1][2][0], self.cube[5][0][0], self.cube[5][1][0], self.cube[5][2][0], self.cube[3][2][2], self.cube[3][1][2], self.cube[3][0][2] = (self.cube[1][0][0], self.cube[1][1][0], self.cube[1][2][0], 
                                                                                                                                                                                                                                                                self.cube[5][0][0], self.cube[5][1][0], self.cube[5][2][0],
                                                                                                                                                                                                                                                                self.cube[3][2][2], self.cube[3][1][2], self.cube[3][0][2],
                                                                                                                                                                                                                                                                self.cube[0][0][0], self.cube[0][1][0], self.cube[0][2][0])
        
        elif dir == -1:
            if face == 0:
                self.cube[1][0], self.cube[2][0], self.cube[3][0], self.cube[4][0] = (self.cube[2][0],
                                                                                    self.cube[3][0],
                                                                                    self.cube[4][0],
                                                                                    self.cube[1][0]
                                                                                    )
            elif face == 5:
                self.cube[1][2], self.cube[2][2], self.cube[3][2], self.cube[4][2] = (self.cube[4][2],
                                                                                      self.cube[1][2],
                                                                                      self.cube[2][2], 
                                                                                      self.cube[3][2])
                                                                                    
            elif face == 1:
                self.cube[0][2][0], self.cube[0][2][1], self.cube[0][2][2], self.cube[2][0][0], self.cube[2][1][0], self.cube[2][2][0], self.cube[5][0][2], self.cube[5][0][1], self.cube[5][0][0], self.cube[4][2][2], self.cube[4][1][2], self.cube[4][0][2] = (self.cube[4][2][2], self.cube[4][1][2], self.cube[4][0][2],
                                                                                                                                                                                                                                                                self.cube[0][2][0], self.cube[0][2][1], self.cube[0][2][2],
                                                                                                                                                                                                                                                                self.cube[2][0][0], self.cube[2][1][0], self.cube[2][2][0],
                                                                                                                                                                                                                                                                self.cube[5][0][2], self.cube[5][0][1], self.cube[5][0][0])
            
            elif face == 3:
                self.cube[0][0][2], self.cube[0][0][1], self.cube[0][0][0], self.cube[4][0][0], self.cube[4][1][0], self.cube[4][2][0], self.cube[5][2][0], self.cube[5][2][1], self.cube[5][2][2], self.cube[2][2][2], self.cube[2][1][2], self.cube[2][0][2] = (self.cube[2][2][2], self.cube[2][1][2], self.cube[2][0][2],
                                                                                                                                                                                                                                                                self.cube[0][0][2], self.cube[0][0][1], self.cube[0][0][0],
                                                                                                                                                                                                                                                                self.cube[4][0][0], self.cube[4][1][0], self.cube[4][2][0],
                                                                                                                                                                                                                                                                self.cube[5][2][0], self.cube[5][2][1], self.cube[5][2][2])
            elif face == 2:
                self.cube[0][2][2], self.cube[0][1][2], self.cube[0][0][2], self.cube[3][0][0], self.cube[3][1][0], self.cube[3][2][0], self.cube[5][2][2], self.cube[5][1][2], self.cube[5][0][2], self.cube[1][2][2], self.cube[1][1][2], self.cube[1][0][2] = (self.cube[1][2][2], self.cube[1][1][2], self.cube[1][0][2],
                                                                                                                                                                                                                                                                self.cube[0][2][2], self.cube[0][1][2], self.cube[0][0][2],
                                                                                                                                                                                                                                                                self.cube[3][0][0], self.cube[3][1][0], self.cube[3][2][0],
                                                                                                                                                                                                                                                                self.cube[5][2][2], self.cube[5][1][2], self.cube[5][0][2])
            elif face == 4:
                self.cube[0][0][0], self.cube[0][1][0], self.cube[0][2][0], self.cube[1][0][0], self.cube[1][1][0], self.cube[1][2][0], self.cube[5][0][0], self.cube[5][1][0], self.cube[5][2][0], self.cube[3][2][2], self.cube[3][1][2], self.cube[3][0][2] = (self.cube[3][2][2], self.cube[3][1][2], self.cube[3][0][2],
                                                                                                                                                                                                                                                                self.cube[0][0][0], self.cube[0][1][0], self.cube[0][2][0],
                                                                                                                                                                                                                                                                self.cube[1][0][0], self.cube[1][1][0], self.cube[1][2][0], 
                                                                                                                                                                                                                                                                self.cube[5][0][0], self.cube[5][1][0], self.cube[5][2][0])


def getRandomScramble(moves: int) -> Cube:
    cube = Cube()
    for i in range(moves):
        dir = random.randint(0, 1)
        face = random.randint(0, 5)
        dir = 1
        face = 1
        if dir == 0:
            cube.rotateFace(face, 1)
        else:
            cube.rotateFace(face, -1)

    return cube