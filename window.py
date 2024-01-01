from ursina import *

ROTATION_SPEED = 200

app = Ursina()

class GUICube():
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
        if not guiCube.rotating:
            guiCube.editRotationCol("w+")
            guiCube.enableRotation()
    elif key == "s":
        if not guiCube.rotating:
            guiCube.editRotationCol("w-")
            guiCube.enableRotation()
    elif key == "r":
        if not guiCube.rotating:
            guiCube.editRotationCol("r+")
            guiCube.enableRotation()
    elif key == "f":
        if not guiCube.rotating:
            guiCube.editRotationCol("r-")
            guiCube.enableRotation()
    elif key == "t":
        if not guiCube.rotating:
            guiCube.editRotationCol("b+")
            guiCube.enableRotation()
    elif key == "g":
        if not guiCube.rotating:
            guiCube.editRotationCol("b-")
            guiCube.enableRotation()
    elif key == "e":
        if not guiCube.rotating:
            guiCube.editRotationCol("g+")
            guiCube.enableRotation()
    elif key == "d":
        if not guiCube.rotating:
            guiCube.editRotationCol("g-")
            guiCube.enableRotation()
    elif key == "y":
        if not guiCube.rotating:
            guiCube.editRotationCol("y+")
            guiCube.enableRotation()
    elif key == "h":
        if not guiCube.rotating:
            guiCube.editRotationCol("y-")
            guiCube.enableRotation()
    elif key == "u":
        if not guiCube.rotating:
            guiCube.editRotationCol("o+")
            guiCube.enableRotation()
    elif key == "j":
        if not guiCube.rotating:
            guiCube.editRotationCol("o-")
            guiCube.enableRotation()

camera.x = 20
camera.y = 20
camera.fov = 30
camera.look_at((0, 0, 0))

app.run()