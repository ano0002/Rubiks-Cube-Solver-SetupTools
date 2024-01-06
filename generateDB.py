import pickle

class CornerCube:
    def __init__(self):
        # Like a 2x2 cube - consider only corners.
        #WRBOGY, as before
        self.corners = [[[0, 0], [0, 0]], 
                        [[1, 1], [1, 1]], 
                        [[2, 2], [2, 2]], 
                        [[3, 3], [3, 3]], 
                        [[4, 4], [4, 4]], 
                        [[5, 5], [5, 5]]]
        
    def generateKey(self) -> str:
        # Key for each corner permutation
        return "".join([str(x) for i in self.corners for j in i for x in j])

    def rotateFace(self, face: int, dir: int) -> None:
        if dir == 1: # Anticlockwise
            self.corners[face] = [list(x) for x in zip(*self.corners[face])][::-1]
            if face == 0:
                self.corners[1][0], self.corners[2][0], self.corners[3][0], self.corners[4][0] = (self.corners[4][0],
                                                                                                  self.corners[1][0], 
                                                                                                  self.corners[2][0], 
                                                                                                  self.corners[3][0])
            elif face == 5:
                self.corners[1][1], self.corners[2][1], self.corners[3][1], self.corners[4][1] = (self.corners[2][1], 
                                                                                                  self.corners[3][1],
                                                                                                  self.corners[4][1],
                                                                                                  self.corners[1][1])
            elif face == 1:
                self.corners[0][1][0], self.corners[0][1][1], self.corners[2][0][0], self.corners[2][1][0], self.corners[5][0][1], self.corners[5][0][0], self.corners[4][1][1], self.corners[4][0][1] = (self.corners[2][0][0], self.corners[2][1][0], 
                                                                                                                                                                                                          self.corners[5][0][1], self.corners[5][0][0], 
                                                                                                                                                                                                          self.corners[4][1][1], self.corners[4][0][1],
                                                                                                                                                                                                          self.corners[0][1][0], self.corners[0][1][1])
            elif face == 3:
                self.corners[0][0][1], self.corners[0][0][0], self.corners[4][0][0], self.corners[4][1][0], self.corners[5][1][0], self.corners[5][1][1], self.corners[2][1][1], self.corners[2][0][1] = (self.corners[4][0][0], self.corners[4][1][0], 
                                                                                                                                                                                                          self.corners[5][1][0], self.corners[5][1][1], 
                                                                                                                                                                                                          self.corners[2][1][1], self.corners[2][0][1],
                                                                                                                                                                                                          self.corners[0][0][1], self.corners[0][0][0])
            elif face == 2:
                self.corners[0][1][1], self.corners[0][0][1], self.corners[3][0][0], self.corners[3][1][0], self.corners[5][1][1], self.corners[5][0][1], self.corners[1][1][1], self.corners[1][0][1] = (self.corners[3][0][0], self.corners[3][1][0], 
                                                                                                                                                                                                          self.corners[5][1][1], self.corners[5][0][1], 
                                                                                                                                                                                                          self.corners[1][1][1], self.corners[1][0][1],
                                                                                                                                                                                                          self.corners[0][1][1], self.corners[0][0][1])
        elif dir == -1: # clockwise
            self.corners[face] = [list(x) for x in zip(*self.corners[face][::-1])]
            if face == 0:
                self.corners[1][0], self.corners[2][0], self.corners[3][0], self.corners[4][0] = (self.corners[2][0], 
                                                                                                  self.corners[3][0],
                                                                                                  self.corners[4][0],
                                                                                                  self.corners[1][0])
            elif face == 5:
                self.corners[1][1], self.corners[2][1], self.corners[3][1], self.corners[4][1] = (self.corners[4][1],
                                                                                                  self.corners[1][1], 
                                                                                                  self.corners[2][1], 
                                                                                                  self.corners[3][1])
            elif face == 1:
                self.corners[0][1][0], self.corners[0][1][1], self.corners[2][0][0], self.corners[2][1][0], self.corners[5][0][1], self.corners[5][0][0], self.corners[4][1][1], self.corners[4][0][1] = (self.corners[4][1][1], self.corners[4][0][1],
                                                                                                                                                                                                          self.corners[0][1][0], self.corners[0][1][1],
                                                                                                                                                                                                          self.corners[2][0][0], self.corners[2][1][0], 
                                                                                                                                                                                                          self.corners[5][0][1], self.corners[5][0][0])
            elif face == 3:
                self.corners[0][0][1], self.corners[0][0][0], self.corners[4][0][0], self.corners[4][1][0], self.corners[5][1][0], self.corners[5][1][1], self.corners[2][1][1], self.corners[2][0][1] = (self.corners[2][1][1], self.corners[2][0][1],
                                                                                                                                                                                                          self.corners[0][0][1], self.corners[0][0][0],
                                                                                                                                                                                                          self.corners[4][0][0], self.corners[4][1][0], 
                                                                                                                                                                                                          self.corners[5][1][0], self.corners[5][1][1])
            elif face == 2:
                self.corners[0][1][1], self.corners[0][0][1], self.corners[3][0][0], self.corners[3][1][0], self.corners[5][1][1], self.corners[5][0][1], self.corners[1][1][1], self.corners[1][0][1] = (self.corners[1][1][1], self.corners[1][0][1],
                                                                                                                                                                                                          self.corners[0][1][1], self.corners[0][0][1],
                                                                                                                                                                                                          self.corners[3][0][0], self.corners[3][1][0], 
                                                                                                                                                                                                          self.corners[5][1][1], self.corners[5][0][1])

def generateDBCorners(corners: list):
    pass