from ursina import *
from thistlethwaite import *
from cube import *
from time import sleep
from threading import Thread
from solutionTools import SolverTools

DEF_ROTATION_SPEED = 400

app = Ursina(development_mode=True, show_ursina_splash=False)

colourMappings = {
    0 : color.white,
    1 : color.red,
    2 : color.blue,
    3 : color.orange,
    4 : color.green,
    5 : color.yellow
}

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
        self.rotationSpeed = 1600
        cube = getRandomScramble(100)
        cube, sol = self.t.Solve(cube)
        print(sol)
        sleep(.1)
        for move in reversed(sol):
            for i in range(move[2]):
                self.rotateFace(move[0], -move[1])
                sleep(.1)
        sleep(2)
        for move in sol:
            for i in range(move[2]):
                self.rotateFace(move[0], move[1])
                sleep(.1)
        
        self.rotationSpeed = DEF_ROTATION_SPEED

            
guiCube = GUICube()

class InputMenu:
    bg = Button(model='quad', scale_x = 2, scale_y = 2.5, scale_z = 0.1, z=1, color=color.dark_gray, disabled=True)
    border = Button(model='quad', scale=0.49, z=0, color=color.black, disabled=True)
    centreButton = Button(model='quad', scale=.15, z=-1, color=color.white)
    paletteBorder = Button(model='quad', scale_x=.17, scale_y=0.62, x=0.5, y=0, z=0, color=color.black, disabled=True, text='Palette', text_origin=(0,0.44), text_color=color.white)
    nextButton = Button(model='quad', text=' Next →', scale_x=.175, scale_y = 0.075, x=0.145, y=-0.375, color=color.black90)
    backButton = Button(model='quad', text='← Back ', disabled=True, visible=False, scale_x=.175, scale_y = 0.075, x=-0.145, y=-0.375, color=color.black90)
    upReference = Button(model='arrow', rotation_z=-90, scale=0.2, scale_x=0.15, y=0.2, z=0, disabled=True, color=color.orange, collider=None)
    downReference = Button(model='arrow', rotation_z=90, scale=0.2, scale_x=0.15, y=-0.2, z=0, disabled=True, color=color.red, collider=None)
    rightReference = Button(model='arrow', rotation_z=0, scale=0.2, scale_x=0.15, x=0.2, z=0, disabled=True, color=color.blue, collider=None)
    leftReference = Button(model='arrow', rotation_z=180, scale=0.2, scale_x=0.15, x=-0.2, z=0, disabled=True, color=color.green, collider=None)
    solveButton = Button(model='quad', text='Solve!', scale_x=.175, scale_y = 0.075, x=0.145, y=-0.375, color=color.black90, disabled=True, visible=False)
    currentFace = 0
    selectedColor = color.white
    faceData = []

    errorBg = Button(model='quad', scale=0.4, scale_x=.7, z=2, disabled=True, visible=False, color=color.color(0.7, 0.7, 0.7, 1), text_origin=(0,0.2), text='ERROR\n\nInvalid cube configuration entered.\nGo back and check all faces are correct!\nUse the coloured arrows to ensure\nthe faces are correctly oriented.')
    errorOk = Button(model='quad', scale_x=.12, z=2, scale_y=0.05, y=-0.1, disabled=True, visible=False, color=color.black66, text='OK', on_click=None)

    def __init__(self) -> None:
        # Input Grid
        self.buttons: list[list[Button]] = []
        for i in range(3):
            row: list[Button] = []
            for j in range(3):
                if not i == j == 1:
                    button = Button(model='quad', scale=.15, color=color.white)
                    button.set_position(((i-1)*3.2, (j-1)*3.2, -1))
                    button.on_click = Func(self.paintColor, button)
                    row.append(button)
                else:
                    row.append(self.centreButton)
            self.buttons.append(row)
        
        self.centreButton.color = color.white
        self.centreButton.highlight_color = color.white
        self.centreButton.pressed_color = color.white

        # Colour Palette
        self.paletteButtons = []
        for i in range(6):
            button = Button(model='quad', scale_x=.15, scale_y=0.075, x=0.5, z=-1, color=color.white)
            button.y = 0.215-(0.0375)*(i+1) - (0.05) * i
            button.color = colourMappings[i]
            button.highlight_color = button.color.tint(.2)
            button.pressed_color = button.color.tint(-.2)
            button.on_click = Func(self.setColor, button)
            self.paletteButtons.append(button)

        # Fonts
        self.paletteBorder.text_entity.font = r'Data\DMSans_36pt-Regular.ttf'
        self.nextButton.text_entity.font = r'Data\DMSans_36pt-Regular.ttf'
        self.backButton.text_entity.font = r'Data\DMSans_36pt-Regular.ttf'
        self.solveButton.text_entity.font = r'Data\DMSans_36pt-Regular.ttf'
        self.errorBg.text_entity.font = r'Data\DMSans_36pt-Regular.ttf'
        self.errorOk.text_entity.font = r'Data\DMSans_36pt-Regular.ttf'

        # Onclick for next and back
        self.nextButton.on_click = Func(self.cycleFace, 1)
        self.backButton.on_click = None

        # Stored faces
        self.faceData = Cube().getState()
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    if j == k == 1:
                        self.faceData[i][j][k] = colourMappings[self.faceData[i][j][k]]
                    else:
                        self.faceData[i][j][k] = color.white
    
    def setColor(self, button: Button):
        self.selectedColor = button.color
    
    def paintColor(self, button: Button):
        button.color = self.selectedColor
        button.highlight_color = button.color.tint(.2)
        button.pressed_color = button.color.tint(-.2)
    
    def cycleFace(self, dir: int):
        # Save edits into stored faces
        for i in range(3):
            for j in range(3):
                if not i == j == 1:
                    self.faceData[self.currentFace][i][j] = self.buttons[i][j].color

        self.currentFace += dir
        self.centreButton.color = colourMappings[self.currentFace]
        self.centreButton.highlight_color = self.centreButton.color
        self.centreButton.pressed_color = self.centreButton.color

        if self.currentFace == 0:
            self.backButton.disabled = True
            self.backButton.on_click = None
            self.backButton.visible = False
        elif self.currentFace == 5:
            self.nextButton.disabled = True
            self.nextButton.on_click = None
            self.nextButton.visible = False
            self.solveButton.disabled = False
            self.solveButton.on_click = self.trySolve
            self.solveButton.z = -1
            self.solveButton.visible = True
        else:
            self.backButton.disabled = False
            self.backButton.on_click = Func(self.cycleFace, -1)
            self.backButton.visible = True
            self.nextButton.disabled = False
            self.nextButton.on_click = Func(self.cycleFace, 1)
            self.nextButton.visible = True
            self.solveButton.disabled = True
            self.solveButton.on_click = None
            self.solveButton.visible = False
            self.solveButton.z = 1

        # Load faces from stored faces
        for i in range(3):
            for j in range(3):
                if not i == j == 1:
                    self.buttons[i][j].color = self.faceData[self.currentFace][i][j]
                    self.buttons[i][j].highlight_color = self.buttons[i][j].color.tint(.2)
                    self.buttons[i][j].pressed_color = self.buttons[i][j].color.tint(-.2)
    
        # Edit reference arrows
        match self.currentFace:
            case 0:
                self.upReference.color = color.orange
                self.rightReference.color = color.blue
                self.downReference.color = color.red
                self.leftReference.color = color.green
            case 1:
                self.upReference.color = color.white
                self.rightReference.color = color.blue
                self.downReference.color = color.yellow
                self.leftReference.color = color.green
            case 2:
                self.upReference.color = color.white
                self.rightReference.color = color.orange
                self.downReference.color = color.yellow
                self.leftReference.color = color.red
            case 3:
                self.upReference.color = color.white
                self.rightReference.color = color.green
                self.downReference.color = color.yellow
                self.leftReference.color = color.blue
            case 4:
                self.upReference.color = color.white
                self.rightReference.color = color.red
                self.downReference.color = color.yellow
                self.leftReference.color = color.orange
            case 5:
                self.upReference.color = color.red
                self.rightReference.color = color.blue
                self.downReference.color = color.orange
                self.leftReference.color = color.green

    def trySolve(self):
        # Save edits of yellow face into stored faces
        for i in range(3):
            for j in range(3):
                if not i == j == 1:
                    self.faceData[self.currentFace][i][j] = self.buttons[i][j].color
                
        invertedMappings = {val:key for key, val in colourMappings.items()}
        regularCube = Cube().getState()
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    regularCube[i][j][k] = invertedMappings[self.faceData[i][j][k]]

        if SolverTools().isCubeValid(Cube(state=regularCube)):
            pass
        else:
            self.showError()
    
    def showError(self):
        self.solveButton.disabled = True
        self.solveButton.on_click = None
        self.backButton.disabled = True
        self.backButton.on_click = None
        for row in self.buttons:
            for button in row:
                button.disabled = True
                button.on_click = None
        self.errorBg.visible = True
        self.errorOk.visible = True
        self.errorOk.disabled = False
        self.errorBg.z = -4
        self.errorOk.z = -5
        self.errorOk.on_click = self.hideError
    
    def hideError(self):
        self.solveButton.disabled = False
        self.solveButton.on_click = self.trySolve
        self.backButton.disabled = False
        self.backButton.on_click = Func(self.cycleFace, -1)
        for row in self.buttons:
            for button in row:
                button.disabled = False
                button.on_click = Func(self.paintColor, button)
        self.errorBg.visible = False
        self.errorOk.visible = False
        self.errorOk.disabled = True
        self.errorBg.z = 4
        self.errorOk.z = 4
        self.errorOk.on_click = None

    def destroySelf(self):
        for row in self.buttons:
            for button in row:
                destroy(button)
        for button in self.paletteButtons:
            destroy(button)
        destroy(self.bg)
        destroy(self.border)
        destroy(self.paletteBorder)
        destroy(self.nextButton)
        destroy(self.backButton)
        destroy(self.upReference)
        destroy(self.downReference)
        destroy(self.rightReference)
        destroy(self.leftReference)
        destroy(self.solveButton)
        destroy(self.errorBg)
        destroy(self.errorOk)


def update():
    global guiCube
    if guiCube.rotating:
        if guiCube.rotating_col == "w+":
            if guiCube.rotation_deg + guiCube.rotationSpeed * time.dt >= 90:
                guiCube.rotateWhite(90-guiCube.rotation_deg)
                guiCube.reIndexWhite(1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateWhite(guiCube.rotationSpeed * time.dt)
                guiCube.editRotationDeg(guiCube.rotationSpeed * time.dt)
        elif guiCube.rotating_col == "w-":
            if guiCube.rotation_deg + guiCube.rotationSpeed * time.dt >= 90:
                guiCube.rotateWhite(guiCube.rotation_deg-90)
                guiCube.reIndexWhite(-1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateWhite(-guiCube.rotationSpeed * time.dt)
                guiCube.editRotationDeg(guiCube.rotationSpeed * time.dt)
        elif guiCube.rotating_col == "b+":
            if guiCube.rotation_deg + guiCube.rotationSpeed * time.dt >= 90:
                guiCube.rotateBlue(90-guiCube.rotation_deg)
                guiCube.reIndexBlue(1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateBlue(guiCube.rotationSpeed * time.dt)
                guiCube.editRotationDeg(guiCube.rotationSpeed * time.dt)
        elif guiCube.rotating_col == "b-":
            if guiCube.rotation_deg + guiCube.rotationSpeed * time.dt >= 90:
                guiCube.rotateBlue(guiCube.rotation_deg-90)
                guiCube.reIndexBlue(-1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateBlue(-guiCube.rotationSpeed * time.dt)
                guiCube.editRotationDeg(guiCube.rotationSpeed * time.dt)
        elif guiCube.rotating_col == "r+":
            if guiCube.rotation_deg + guiCube.rotationSpeed * time.dt >= 90:
                guiCube.rotateRed(90-guiCube.rotation_deg)
                guiCube.reIndexRed(1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateRed(guiCube.rotationSpeed * time.dt)
                guiCube.editRotationDeg(guiCube.rotationSpeed * time.dt)
        elif guiCube.rotating_col == "r-":
            if guiCube.rotation_deg + guiCube.rotationSpeed * time.dt >= 90:
                guiCube.rotateRed(guiCube.rotation_deg-90)
                guiCube.reIndexRed(-1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateRed(-guiCube.rotationSpeed * time.dt)
                guiCube.editRotationDeg(guiCube.rotationSpeed * time.dt)
        elif guiCube.rotating_col == "g+":
            if guiCube.rotation_deg + guiCube.rotationSpeed * time.dt >= 90:
                guiCube.rotateGreen(90-guiCube.rotation_deg)
                guiCube.reIndexGreen(1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateGreen(guiCube.rotationSpeed * time.dt)
                guiCube.editRotationDeg(guiCube.rotationSpeed * time.dt)
        elif guiCube.rotating_col == "g-":
            if guiCube.rotation_deg + guiCube.rotationSpeed * time.dt >= 90:
                guiCube.rotateGreen(guiCube.rotation_deg-90)
                guiCube.reIndexGreen(-1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateGreen(-guiCube.rotationSpeed * time.dt)
                guiCube.editRotationDeg(guiCube.rotationSpeed * time.dt)
        elif guiCube.rotating_col == "y+":
            if guiCube.rotation_deg + guiCube.rotationSpeed * time.dt >= 90:
                guiCube.rotateYellow(90-guiCube.rotation_deg)
                guiCube.reIndexYellow(1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateYellow(guiCube.rotationSpeed * time.dt)
                guiCube.editRotationDeg(guiCube.rotationSpeed * time.dt)
        elif guiCube.rotating_col == "y-":
            if guiCube.rotation_deg + guiCube.rotationSpeed * time.dt >= 90:
                guiCube.rotateYellow(guiCube.rotation_deg-90)
                guiCube.reIndexYellow(-1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateYellow(-guiCube.rotationSpeed * time.dt)
                guiCube.editRotationDeg(guiCube.rotationSpeed * time.dt)
        elif guiCube.rotating_col == "o+":
            if guiCube.rotation_deg + guiCube.rotationSpeed * time.dt >= 90:
                guiCube.rotateOrange(90-guiCube.rotation_deg)
                guiCube.reIndexOrange(1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateOrange(guiCube.rotationSpeed * time.dt)
                guiCube.editRotationDeg(guiCube.rotationSpeed * time.dt)
        elif guiCube.rotating_col == "o-":
            if guiCube.rotation_deg + guiCube.rotationSpeed * time.dt >= 90:
                guiCube.rotateOrange(guiCube.rotation_deg-90)
                guiCube.reIndexOrange(-1)
                guiCube.disableRotation()
                guiCube.resetRotationDeg()
            else:
                guiCube.rotateOrange(-guiCube.rotationSpeed * time.dt)
                guiCube.editRotationDeg(guiCube.rotationSpeed * time.dt)

def input(key):
    global guiCube
    global i
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
            t.daemon = True
            t.start()
    elif key == "l":
        i.destroySelf()


camera.x = 20
camera.y = 20
camera.fov = 25
camera.look_at((0, 0, 0))

i = InputMenu()
#i.destroySelf()

app.run()