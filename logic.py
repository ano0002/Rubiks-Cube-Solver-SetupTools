class Cube:
    def __init__(self) -> None:
        self.cube = [[[]]]
        #WRBOGY
        #012345

    def rotateFace(self, face: int, dir: int):
        if dir == 1:
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
                self.cube[1][2], self.cube[2][2], self.cube[3][2], self.cube[4][2] = (self.cube[4][2],
                                                                                    self.cube[1][2],
                                                                                    self.cube[2][2],
                                                                                    self.cube[3][2]
                                                                                    )
            elif face == 1:
                self.cube[0][2][0], self.cube[0][2][1], self.cube[0][2][2], 
                self.cube[2][0][0], self.cube[2][1][0], self.cube[2][2][0],
                self.cube[5][0][2], self.cube[5][0][1], self.cube[5][0][0],
                self.cube[4][0][2], self.cube[4][1][2], self.cube[4][2][2] = (self.cube[2][0][0], self.cube[2][1][0], self.cube[2][2][0],
                                                                            self.cube[5][0][2], self.cube[5][0][1], self.cube[5][0][0],
                                                                            self.cube[4][0][2], self.cube[4][1][2], self.cube[4][2][2],
                                                                            self.cube[0][2][0], self.cube[0][2][1], self.cube[0][2][2])
                