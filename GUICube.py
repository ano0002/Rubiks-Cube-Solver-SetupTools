from ursina import *
from thistlethwaite import *
from time import sleep

DEF_ROTATION_SPEED = 400

class GUICube():
    t = Thistlethwaite()
    rotationSpeed = DEF_ROTATION_SPEED

    def __init__(self) -> None:
        cubepiece = Entity(model='cube', color=color.black)
        blueplate = Entity(model="cube", scale_x=0.9, scale_y=0.9, scale_z=0.1, z=-0.5, color=color.blue, parent=cubepiece)
        yellowplate = Entity(model="cube", scale_x=0.1, scale_y=0.9, scale_z=0.9, x=-0.5, color=color.yellow, parent=cubepiece)
        redplate = Entity(model="cube", scale_x=0.9, scale_y=0.1, scale_z=0.9, y=0.5, color=color.red, parent=cubepiece)
        whiteplate = Entity(model="cube", scale_x=0.1, scale_y=0.9, scale_z=0.9, x=0.5, color=color.white, parent=cubepiece)
        orangeplate = Entity(model="cube", scale_x=0.9, scale_y=0.1, scale_z=0.9, y=-0.5, color=color.orange, parent=cubepiece)
        greenplate = Entity(model="cube", scale_x=0.9, scale_y=0.9, scale_z=0.1, z=0.5, color=color.green, parent=cubepiece)

        self.cube = []
        for i in range(3):
            layer = []
            for j in range(3):
                line = []
                for k in range(3):
                    piece = duplicate(cubepiece)
                    piece.set_position((i-1, j-1, k-1))
                    line.append(piece)
                layer.append(line)
            self.cube.append(layer)

        destroy(cubepiece)

        for layer in self.cube:
            for line in layer:
                for piece in line:
                    if piece != self.cube[1][1][1]:
                        piece.world_parent = self.cube[1][1][1]
        
        self.rotating = False
        self.rotating_col = None
        self.rotation_deg = 0

    def rotateYellow(self, scale: int) -> None:
        for line in self.cube[0]:
            for piece in line:
                if piece != self.cube[0][1][1]:
                    piece.world_parent = self.cube[0][1][1]
        self.cube[0][1][1].rotation_x += scale * 1
        for line in self.cube[0]:
            for piece in line:
                piece.world_parent = self.cube[1][1][1]

    def reIndexYellow(self, scale: int) -> None:
        #rearrange cube indices
        #Anti-clockwise -> transpose then reverse
        #Clockwise -> reverse then transpose
        if scale > 0:
            self.cube[0] = list(list(x) for x in zip(*self.cube[0]))[::-1]
        else:
            self.cube[0] = list(list(x) for x in zip(*(self.cube[0][::-1])))

    def rotateWhite(self, scale: int) -> None:
        for line in self.cube[2]:
            for piece in line:
                if piece != self.cube[2][1][1]:
                    piece.world_parent = self.cube[2][1][1]
        self.cube[2][1][1].rotation_x += scale * 1
        for line in self.cube[2]:
            for piece in line:
                piece.world_parent = self.cube[1][1][1]

    def reIndexWhite(self, scale: int) -> None:
        #rearrange cube indices
        #Anti-clockwise -> transpose then reverse
        #Clockwise -> reverse then transpose
        if scale > 0:
            self.cube[2] = list(list(x) for x in zip(*self.cube[2]))[::-1]
        else:
            self.cube[2] = list(list(x) for x in zip(*(self.cube[2][::-1])))

    def rotateBlue(self, scale: int) -> None:
        for i in range(3):
            for k in range(3):
                if i != 1 or k != 1:
                    self.cube[i][k][0].world_parent = self.cube[1][1][0]
        self.cube[1][1][0].rotation_z -= scale * 1
        for i in range(3):
            for k in range(3):
                self.cube[i][k][0].world_parent = self.cube[1][1][1]
        
    def reIndexBlue(self, scale: int) -> None:
        # make cube[0] the blue face
        self.cube[0] = list(list(x) for x in zip(*self.cube[0]))
        self.cube[1] = list(list(x) for x in zip(*self.cube[1]))
        self.cube[2] = list(list(x) for x in zip(*self.cube[2]))
        self.cube = list(list(x) for x in zip(*self.cube)) 

        #rearrange cube indices, rotations as before
        if scale > 0:
            self.cube[0] = list(list(x) for x in zip(*self.cube[0]))[::-1]
        else:
            self.cube[0] = list(list(x) for x in zip(*(self.cube[0][::-1])))
        
        # revert to original layout
        self.cube = list(list(x) for x in zip(*self.cube)) 
        self.cube[0] = list(list(x) for x in zip(*self.cube[0]))
        self.cube[1] = list(list(x) for x in zip(*self.cube[1]))
        self.cube[2] = list(list(x) for x in zip(*self.cube[2]))

    def rotateGreen(self, scale: int) -> None:
        for i in range(3):
            for k in range(3):
                if i != 1 or k != 1:
                    self.cube[i][k][2].world_parent = self.cube[1][1][2]
        self.cube[1][1][2].rotation_z -= scale * 1
        for i in range(3):
            for k in range(3):
                self.cube[i][k][2].world_parent = self.cube[1][1][1]
        
    def reIndexGreen(self, scale: int) -> None:
        # make cube[2] the green face
        self.cube[0] = list(list(x) for x in zip(*self.cube[0]))
        self.cube[1] = list(list(x) for x in zip(*self.cube[1]))
        self.cube[2] = list(list(x) for x in zip(*self.cube[2]))
        self.cube = list(list(x) for x in zip(*self.cube)) 

        #rearrange cube indices, rotations as before
        if scale > 0:
            self.cube[2] = list(list(x) for x in zip(*self.cube[2]))[::-1]
        else:
            self.cube[2] = list(list(x) for x in zip(*(self.cube[2][::-1])))
        
        # revert to original layout
        self.cube = list(list(x) for x in zip(*self.cube)) 
        self.cube[0] = list(list(x) for x in zip(*self.cube[0]))
        self.cube[1] = list(list(x) for x in zip(*self.cube[1]))
        self.cube[2] = list(list(x) for x in zip(*self.cube[2]))

    def rotateOrange(self, scale: int) -> None:
        for i in range(3):
            for k in range(3):
                if i != 1 or k != 1:
                    self.cube[i][0][k].world_parent = self.cube[1][0][1]
        self.cube[1][0][1].rotation_y += scale * 1
        for i in range(3):
            for k in range(3):
                self.cube[i][0][k].world_parent = self.cube[1][1][1]
        
    def reIndexOrange(self, scale: int) -> None:
        #make cube[0] the orange face
        self.cube = list(list(x) for x in zip(*self.cube)) 

        #rotate as usual
        if scale < 0:
            self.cube[0] = list(list(x) for x in zip(*self.cube[0]))[::-1]
        else:
            self.cube[0] = list(list(x) for x in zip(*(self.cube[0][::-1])))
        
        #revert
        self.cube = list(list(x) for x in zip(*self.cube)) 

    def rotateRed(self, scale: int) -> None:
        for i in range(3):
            for k in range(3):
                if i != 1 or k != 1:
                    self.cube[i][2][k].world_parent = self.cube[1][2][1]
        self.cube[1][2][1].rotation_y += scale * 1
        for i in range(3):
            for k in range(3):
                self.cube[i][2][k].world_parent = self.cube[1][1][1]
        
    def reIndexRed(self, scale: int) -> None:
        #make cube[2] the red face
        self.cube = list(list(x) for x in zip(*self.cube)) 

        #rotate as usual
        if scale < 0:
            self.cube[2] = list(list(x) for x in zip(*self.cube[2]))[::-1]
        else:
            self.cube[2] = list(list(x) for x in zip(*(self.cube[2][::-1])))
        
        #revert
        self.cube = list(list(x) for x in zip(*self.cube)) 

    def rotateFace(self, face: int, dir: int) -> None:
        if not self.rotating:
            match face:
                case 0:
                    if dir == -1:
                        self.editRotationCol("w+")
                    else:
                        self.editRotationCol("w-")
                
                case 1:
                    if dir == -1:
                        self.editRotationCol("r+")
                    else:
                        self.editRotationCol("r-")

                case 2:
                    if dir == 1:
                        self.editRotationCol("b+")
                    else:
                        self.editRotationCol("b-")

                case 3:
                    if dir == 1:
                        self.editRotationCol("o+")
                    else:
                        self.editRotationCol("o-")

                case 4:
                    if dir == -1:
                        self.editRotationCol("g+")
                    else:
                        self.editRotationCol("g-")

                case 5:
                    if dir == 1:
                        self.editRotationCol("y+")
                    else:
                        self.editRotationCol("y-")
            
            self.enableRotation()
    
    def rotateCubeUp(self) -> None:
        self.cube[1][1][1].rotation_x += 45
    
    def rotateCubeDown(self) -> None:
        self.cube[1][1][1].rotation_x -= 45
    
    def rotateCubeLeft(self) -> None:
        self.cube[1][1][1].rotation_y += 45

    def rotateCubeRight(self) -> None:
        self.cube[1][1][1].rotation_y -= 45

    def enableRotation(self) -> None:
        self.rotating = True
    
    def disableRotation(self) -> None:
        self.rotating = False
    
    def editRotationDeg(self, deg:int) -> None:
        self.rotation_deg += deg
    
    def resetRotationDeg(self) -> None:
        self.rotation_deg = 0
    
    def editRotationCol(self, col:str) -> None:
        self.rotating_col = col

    def scrambleToSolution(self, solution: list):
        self.rotationSpeed = 1600
        sleep(1)
        print(solution)
        for move in reversed(solution):
            if move != 'END':
                for _ in range(move[2]):
                    self.rotateFace(move[0], -move[1])
                    sleep(.1)

        self.rotationSpeed = DEF_ROTATION_SPEED
    
    def scrambleAndSolve(self):
        self.rotationSpeed = 1600
        cube = getRandomScramble(100)
        cube, sol = self.t.Solve(cube)
        print(sol)
        sleep(.1)
        for move in reversed(sol):
            for _ in range(move[2]):
                self.rotateFace(move[0], -move[1])
                sleep(.1)
        sleep(2)
        for move in sol:
            for i in range(move[2]):
                self.rotateFace(move[0], move[1])
                sleep(.1)
        
        self.rotationSpeed = DEF_ROTATION_SPEED