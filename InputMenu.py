from ursina import *
from solutionTools import SolverTools
from cube import Cube
from thistlethwaite import *
from threading import Thread

colourMappings = {
    0 : color.white,
    1 : color.red,
    2 : color.blue,
    3 : color.orange,
    4 : color.green,
    5 : color.yellow
}
titleMappings = {
    0 : "white",
    1 : "red",
    2 : "blue",
    3 : "orange",
    4 : "green",
    5 : "yellow"
}

class InputMenu:
    def __init__(self, solution: list) -> None:
        # Buttons and stuff
        self.bg = Button(model='quad', scale_x = 2, scale_y = 2.5, scale_z = 0.1, z=1, color=color.dark_gray, disabled=True, collider=None)
        self.border = Button(model='quad', scale=0.49, z=0, color=color.black, disabled=True, collider=None)
        self.centreButton = Button(model='quad', scale=.15, z=-1, color=color.white)
        self.paletteBorder = Button(model='quad', scale_x=.17, scale_y=0.62, x=0.5, y=0, z=0, color=color.black, disabled=True, text='Palette', text_origin=(0,0.44), text_color=color.white, collider=None)
        self.nextButton = Button(model='quad', text=' Next →', scale_x=.175, scale_y = 0.075, x=0.145, y=-0.375, color=color.black90)
        self.backButton = Button(model='quad', text='← Back ', disabled=True, visible=False, scale_x=.175, scale_y = 0.075, x=-0.145, y=-0.375, color=color.black90)
        self.upReference = Button(model='arrow', rotation_z=-90, scale=0.2, scale_x=0.15, y=0.2, z=0, disabled=True, color=color.orange, collider=None)
        self.downReference = Button(model='arrow', rotation_z=90, scale=0.2, scale_x=0.15, y=-0.2, z=0, disabled=True, color=color.red, collider=None)
        self.rightReference = Button(model='arrow', rotation_z=0, scale=0.2, scale_x=0.15, x=0.2, z=0, disabled=True, color=color.blue, collider=None)
        self.leftReference = Button(model='arrow', rotation_z=180, scale=0.2, scale_x=0.15, x=-0.2, z=0, disabled=True, color=color.green, collider=None)
        self.solveButton = Button(model='quad', text='Solve!', scale_x=.175, scale_y = 0.075, x=0.145, y=-0.375, color=color.black90, disabled=True, visible=False)
        self.currentFace = 0
        self.selectedColor = color.white
        self.faceData = []

        # Instructions
        instructionstext = "Enter the faces of your cube!\n\nThe centre piece of a face determines that face's color.\n\nUse the coloured arrows that denote the color of the adjacent faces to ensure you are entering a face in the correct orientation."

        self.instructions = Text(text=instructionstext, wordwrap=20, size=.04, x=-0.8, y=0.28)

        # For output
        self.solution = solution

        self.errorBg = Button(model='quad', scale=0.4, scale_x=.7, z=2, disabled=True, visible=False, color=color.color(0.7, 0.7, 0.7, 1), text_origin=(0,0.2), text='ERROR\n\nInvalid cube configuration entered.\nGo back and check all faces are correct!\nUse the coloured arrows to ensure\nthe faces are correctly oriented.')
        self.errorOk = Button(model='quad', scale_x=.12, z=2, scale_y=0.05, y=-0.1, disabled=True, visible=False, color=color.black66, text='OK', on_click=None)

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
        self.paletteBorder.text_entity.font = r'Data\DMSans36pt-Regular.ttf'
        self.nextButton.text_entity.font = r'Data\DMSans36pt-Regular.ttf'
        self.backButton.text_entity.font = r'Data\DMSans36pt-Regular.ttf'
        self.solveButton.text_entity.font = r'Data\DMSans36pt-Regular.ttf'
        self.errorBg.text_entity.font = r'Data\DMSans36pt-Regular.ttf'
        self.errorOk.text_entity.font = r'Data\DMSans36pt-Regular.ttf'
        self.instructions.font = r'Data\DMSans36pt-Regular.ttf'

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
        
        self.updateTitle()
    
    def setColor(self, button: Button):
        self.selectedColor = button.color
    
    def updateTitle(self):
        # Title
        # Delete all existing letters if possible
        try:
            for letter in self.letters:
                destroy(letter)
            self.letters = []
        except:
            pass

        text = f"enter {titleMappings[self.currentFace]} face"
        y = 0.42
        titletext = dedent(text)

        Text.default_font = r"Data\CurvedSquare-eDzl.ttf"
        Text.default_resolution = 4320 * Text.size

        title = Text(size=.08)
        title.text = titletext
        fullwidth = title.width

        destroy(title)
        toggleTitleColor = False
        self.letters = []
        colors = [color.white, color.red, color.blue, color.orange, color.green, color.yellow]
        col_i = 0
        for i, char in enumerate(text):
            letter = Text(size=.08)
            letter.text = dedent(char)
            letter.x = -fullwidth/2 + i*(fullwidth/len(text))
            letter.y = y
            
            if char != " ":
                if not toggleTitleColor:
                    letter.color = colors[col_i]
                    col_i += 1
                    col_i %= len(colors)
                else:
                    letter.color = colors[self.currentFace]
            else:
                toggleTitleColor = not toggleTitleColor
            
            self.letters.append(letter)
    
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

        self.updateTitle()

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
                    regularCube[i][k][j] = invertedMappings[self.faceData[i][j][k]]

        regularCube = [list(x)[::-1] for x in regularCube] # Face data needs to be mapped differently
        
        if SolverTools().isCubeValid(Cube(state=regularCube)):
            if not SolverTools().isSolved(Cube(state=regularCube)):
                t = Thread(target=self.Solve, args=[Cube(state=regularCube)])
                t.daemon = True
                t.start()
            else:
                self.showSolvedError()
        else:
            self.showError()
    
    def ReceiveSolution(self, moves: list):
        if len(moves) == 0:
            self.showError()
        else:
            for move in moves:
                self.solution.append(move)
            self.solution.append('END') # END flag
            self.destroySelf()
    
    def Solve(self, cube: Cube):
        t = Thistlethwaite()
        try:
            _, result = t.Solve(cube, terminate_after=5)
            self.ReceiveSolution(result)
            return None
        except TimeoutError:
            self.ReceiveSolution([])
            return None
        except Exception as e:
            print(e)
            return None

    def showSolvedError(self):
        self.solveButton.disabled = True
        self.solveButton.on_click = None
        self.backButton.disabled = True
        self.backButton.on_click = None
        for row in self.buttons:
            for button in row:
                button.disabled = True
                button.on_click = None
        self.errorBg.text = 'ERROR\n\nThe cube you entered is already solved!\nGo back and enter an unsolved cube.\nUse the coloured arrows to ensure\nthe faces are correctly oriented.'
        self.errorBg.visible = True
        self.errorOk.visible = True
        self.errorOk.disabled = False
        self.errorBg.z = -4
        self.errorOk.z = -5
        self.errorOk.on_click = self.hideSolvedError
    
    def hideSolvedError(self):
        self.solveButton.disabled = False
        self.solveButton.on_click = self.trySolve
        self.backButton.disabled = False
        self.backButton.on_click = Func(self.cycleFace, -1)
        for row in self.buttons:
            for button in row:
                button.disabled = False
                button.on_click = Func(self.paintColor, button)
        self.errorBg.visible = False
        self.errorBg.text = 'ERROR\n\nInvalid cube configuration entered.\nGo back and check all faces are correct!\nUse the coloured arrows to ensure\nthe faces are correctly oriented.'
        self.errorOk.visible = False
        self.errorOk.disabled = True
        self.errorBg.z = 4
        self.errorOk.z = 4
        self.errorOk.on_click = None

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
        for letter in self.letters:
            destroy(letter)
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
        destroy(self.instructions)
