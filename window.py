from ursina import *
from thistlethwaite import *
from cube import *
from time import sleep
from threading import Thread

ROTATION_SPEED = 400

app = Ursina(development_mode=True)

class GUICube():
    t = Thistlethwaite()

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
                    if dir == 1:
                        self.editRotationCol("w+")
                    else:
                        self.editRotationCol("w-")
                
                case 1:
                    if dir == 1:
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
                    if dir == 1:
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
    
    def scrambleAndSolve(self):
        cube = getRandomScramble(100)
        cube, sol = self.t.Solve(cube)
        print(sol)
        sleep(.1)
        for move in reversed(sol):
            for i in range(move[2]):
                self.rotateFace(move[0], -move[1])
                sleep(.3)
        sleep(2)
        for move in sol:
            for i in range(move[2]):
                self.rotateFace(move[0], move[1])
                sleep(.3)

            
guiCube = GUICube()

def update():
    global guiCube
    if guiCube.rotating:
        if guiCube.rotating_col == "w+":
            if guiCube.rotation_deg + ROTATION_SPEED * time.dt >= 90:
                guiCube.rotateWhite(90-guiCube.rotation_deg)
                guiCube.reIndexWhite(1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateWhite(ROTATION_SPEED * time.dt)
                guiCube.editRotationDeg(ROTATION_SPEED * time.dt)
        elif guiCube.rotating_col == "w-":
            if guiCube.rotation_deg + ROTATION_SPEED * time.dt >= 90:
                guiCube.rotateWhite(guiCube.rotation_deg-90)
                guiCube.reIndexWhite(-1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateWhite(-ROTATION_SPEED * time.dt)
                guiCube.editRotationDeg(ROTATION_SPEED * time.dt)
        elif guiCube.rotating_col == "b+":
            if guiCube.rotation_deg + ROTATION_SPEED * time.dt >= 90:
                guiCube.rotateBlue(90-guiCube.rotation_deg)
                guiCube.reIndexBlue(1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateBlue(ROTATION_SPEED * time.dt)
                guiCube.editRotationDeg(ROTATION_SPEED * time.dt)
        elif guiCube.rotating_col == "b-":
            if guiCube.rotation_deg + ROTATION_SPEED * time.dt >= 90:
                guiCube.rotateBlue(guiCube.rotation_deg-90)
                guiCube.reIndexBlue(-1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateBlue(-ROTATION_SPEED * time.dt)
                guiCube.editRotationDeg(ROTATION_SPEED * time.dt)
        elif guiCube.rotating_col == "r+":
            if guiCube.rotation_deg + ROTATION_SPEED * time.dt >= 90:
                guiCube.rotateRed(90-guiCube.rotation_deg)
                guiCube.reIndexRed(1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateRed(ROTATION_SPEED * time.dt)
                guiCube.editRotationDeg(ROTATION_SPEED * time.dt)
        elif guiCube.rotating_col == "r-":
            if guiCube.rotation_deg + ROTATION_SPEED * time.dt >= 90:
                guiCube.rotateRed(guiCube.rotation_deg-90)
                guiCube.reIndexRed(-1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateRed(-ROTATION_SPEED * time.dt)
                guiCube.editRotationDeg(ROTATION_SPEED * time.dt)
        elif guiCube.rotating_col == "g+":
            if guiCube.rotation_deg + ROTATION_SPEED * time.dt >= 90:
                guiCube.rotateGreen(90-guiCube.rotation_deg)
                guiCube.reIndexGreen(1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateGreen(ROTATION_SPEED * time.dt)
                guiCube.editRotationDeg(ROTATION_SPEED * time.dt)
        elif guiCube.rotating_col == "g-":
            if guiCube.rotation_deg + ROTATION_SPEED * time.dt >= 90:
                guiCube.rotateGreen(guiCube.rotation_deg-90)
                guiCube.reIndexGreen(-1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateGreen(-ROTATION_SPEED * time.dt)
                guiCube.editRotationDeg(ROTATION_SPEED * time.dt)
        elif guiCube.rotating_col == "y+":
            if guiCube.rotation_deg + ROTATION_SPEED * time.dt >= 90:
                guiCube.rotateYellow(90-guiCube.rotation_deg)
                guiCube.reIndexYellow(1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateYellow(ROTATION_SPEED * time.dt)
                guiCube.editRotationDeg(ROTATION_SPEED * time.dt)
        elif guiCube.rotating_col == "y-":
            if guiCube.rotation_deg + ROTATION_SPEED * time.dt >= 90:
                guiCube.rotateYellow(guiCube.rotation_deg-90)
                guiCube.reIndexYellow(-1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateYellow(-ROTATION_SPEED * time.dt)
                guiCube.editRotationDeg(ROTATION_SPEED * time.dt)
        elif guiCube.rotating_col == "o+":
            if guiCube.rotation_deg + ROTATION_SPEED * time.dt >= 90:
                guiCube.rotateOrange(90-guiCube.rotation_deg)
                guiCube.reIndexOrange(1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateOrange(ROTATION_SPEED * time.dt)
                guiCube.editRotationDeg(ROTATION_SPEED * time.dt)
        elif guiCube.rotating_col == "o-":
            if guiCube.rotation_deg + ROTATION_SPEED * time.dt >= 90:
                guiCube.rotateOrange(guiCube.rotation_deg-90)
                guiCube.reIndexOrange(-1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateOrange(-ROTATION_SPEED * time.dt)
                guiCube.editRotationDeg(ROTATION_SPEED * time.dt)

def input(key):
    global guiCube
    if key == "up arrow":
        guiCube.rotateCubeUp()
    elif key == "down arrow":
        guiCube.rotateCubeDown()
    elif key == "left arrow":
        guiCube.rotateCubeLeft()
    elif key == "right arrow":
        guiCube.rotateCubeRight()
    elif key == "w":
        guiCube.rotateFace(0, 1)
    elif key == "s":
        guiCube.rotateFace(0, -1)
    elif key == "r":
        guiCube.rotateFace(1, 1)
    elif key == "f":
        guiCube.rotateFace(1, -1)
    elif key == "t":
        guiCube.rotateFace(2, 1)
    elif key == "g":
        guiCube.rotateFace(2, -1)
    elif key == "e":
        guiCube.rotateFace(3, 1)
    elif key == "d":
        guiCube.rotateFace(3, -1)
    elif key == "y":
        guiCube.rotateFace(4, 1)
    elif key == "h":
        guiCube.rotateFace(4, -1)
    elif key == "u":
        guiCube.rotateFace(5, 1)
    elif key == "j":
        guiCube.rotateFace(5, -1)
    elif key == "b":
        if not guiCube.rotating:
            t = Thread(target=guiCube.scrambleAndSolve)
            t.start()

camera.x = 20
camera.y = 20
camera.fov = 30
camera.look_at((0, 0, 0))

app.run()