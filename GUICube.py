from ursina import *
from thistlethwaite import *
from time import sleep
from threading import Thread

class GUICube():
    t = Thistlethwaite()

    def __init__(self, exitCode: list, defaultRotationSpeed: int=400) -> None:
        cubepiece = Entity(model='cube', color=color.black)
        blueplate = Entity(model="cube", scale_x=0.9, scale_y=0.9, scale_z=0.1, z=-0.5, color=color.blue, parent=cubepiece)
        yellowplate = Entity(model="cube", scale_x=0.1, scale_y=0.9, scale_z=0.9, x=-0.5, color=color.yellow, parent=cubepiece)
        redplate = Entity(model="cube", scale_x=0.9, scale_y=0.1, scale_z=0.9, y=0.5, color=color.red, parent=cubepiece)
        whiteplate = Entity(model="cube", scale_x=0.1, scale_y=0.9, scale_z=0.9, x=0.5, color=color.white, parent=cubepiece)
        orangeplate = Entity(model="cube", scale_x=0.9, scale_y=0.1, scale_z=0.9, y=-0.5, color=color.orange, parent=cubepiece)
        greenplate = Entity(model="cube", scale_x=0.9, scale_y=0.9, scale_z=0.1, z=0.5, color=color.green, parent=cubepiece)

        self.exitCode = exitCode

        self.rotationSpeed = defaultRotationSpeed
        self.defaultRotationSpeed = defaultRotationSpeed

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

        # Buttons for showing solution
        self.start = Button(model='quad', text=' Start →', visible=False, scale_x=.175, scale_y = 0.075, x=0.245, y=-0.375, color=color.black90)
        self.next = Button(model='quad', text=' Next →', disabled=True, visible=False, scale_x=.175, scale_y = 0.075, x=0.245, y=-0.375, color=color.black90)
        self.done = Button(model='quad', text=' Done ', disabled=True, visible=False, scale_x=.175, scale_y = 0.075, x=0.245, y=-0.375, color=color.black90)
        self.back = Button(model='quad', text='← Back ', disabled=True, visible=False, scale_x=.175, scale_y = 0.075, x=-0.245, y=-0.375, color=color.black90)
        self.replay = Button(model='quad', text='⟳ Replay ', disabled=True, visible=False, scale_x=.175, scale_y = 0.075, x=0, y=-0.375, z=1, color=color.black90)
        self.start.text_entity.font = r'Data\DMSans36pt-Regular.ttf'
        self.next.text_entity.font = r'Data\DMSans36pt-Regular.ttf'
        self.done.text_entity.font = r'Data\DMSans36pt-Regular.ttf'
        self.back.text_entity.font = r'Data\DMSans36pt-Regular.ttf'
        self.replay.text_entity.font = r'Data\DMSans36pt-Regular.ttf'

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

        self.rotationSpeed = self.defaultRotationSpeed

        self.showSolution(solution)
    
    def showSolution(self, solution: list):        
        self.start.visible = True
        self.replay.z = 0

        self.moveIndex = 0
        self.solution = solution
        self.start.on_click = self.threadNext

        y = 0.42
        slashtext = dedent("/")

        Text.default_font = r"Data\CurvedSquare-eDzl.ttf"
        Text.default_resolution = 4320 * Text.size

        self.slash = Text(size=.08, y=y, color=color.white)
        self.slash.text = slashtext
        self.slash.x = -0.5*self.slash.width
        self.moveCount = []
        self.updateMoveCount()
    
    def updateMoveCount(self):
        # Delete all existing numbers if possible
        try:
            for letter in self.moveCount:
                destroy(letter)
            self.moveCount = []
        except:
            pass

        text = f"{self.moveIndex+1}"
        y = 0.42
        text = dedent(text)

        Text.default_font = r"Data\CurvedSquare-eDzl.ttf"
        Text.default_resolution = 4320 * Text.size

        title = Text(size=.08)
        title.text = text
        fullwidth = title.width
        destroy(title)

        colors = [color.red, color.blue, color.orange, color.green, color.yellow]
        col_i = 0
        for i, char in enumerate(text):
            letter = Text(size=.08)
            letter.text = dedent(char)
            letter.x = -fullwidth -0.5*(fullwidth/len(text)) + i*(fullwidth/len(text))
            letter.y = y
            letter.color = colors[col_i]
            col_i += 1
            col_i %= len(colors)
            self.moveCount.append(letter)
        
        text = f"{len(self.solution)}"
        y = 0.42
        text = dedent(text)

        Text.default_font = r"Data\CurvedSquare-eDzl.ttf"
        Text.default_resolution = 4320 * Text.size

        title = Text(size=.08)
        title.text = text
        fullwidth = title.width
        destroy(title)

        for i, char in enumerate(text):
            letter = Text(size=.08)
            letter.text = dedent(char)
            letter.x = 0.5*(fullwidth/len(text)) + i*(fullwidth/len(text))
            letter.y = y
            letter.color = colors[col_i]
            col_i += 1
            col_i %= len(colors)
            self.moveCount.append(letter)

    def threadNext(self):
        t = Thread(target=self.nextMove)
        t.daemon = True
        t.start()
    
    def threadPrev(self):
        t = Thread(target=self.prevMove)
        t.daemon = True
        t.start()

    def threadReplay(self):
        t = Thread(target=self.replayMove)
        t.daemon = True
        t.start()

    def replayMove(self):
        if not self.rotating:
            # Disable buttons whilst rotating
            self.start.on_click = None
            self.next.on_click = None
            self.back.on_click = None
            self.replay.on_click = None
            move = self.solution[self.moveIndex-1]

            # Reset with no animation
            self.rotationSpeed = 1000000
            for _ in range(move[2]):
                self.rotateFace(move[0], -move[1])
                sleep(time.dt)
            self.rotationSpeed = self.defaultRotationSpeed

            sleep(.5)

            # Show move normally
            sleep(.2)
            for _ in range(move[2]):
                self.rotateFace(move[0], move[1])
                sleep(.3)

            # Re-enable buttons
            if self.moveIndex == len(self.solution) - 1:
                self.done.on_click = self.returnToMenu
                self.done.visible = True
                self.done.disabled = False
                self.done.z = 0
                
                self.next.on_click = None
                self.next.visible = False
                self.next.disabled = True
                self.next.z = 1

                self.back.on_click = self.threadPrev
                self.back.visible = True
                self.back.disabled = False

                self.replay.on_click = self.threadReplay
                self.replay.visible = True
                self.replay.disabled = False

                self.start.on_click = None
                self.start.z = 1
                self.start.visible = False
                self.start.disabled = True

            elif self.moveIndex >= 1:
                self.start.on_click = None
                self.start.z = 1
                self.start.visible = False
                self.start.disabled = True

                self.next.on_click = self.threadNext
                self.next.visible = True
                self.next.disabled = False

                self.back.on_click = self.threadPrev
                self.back.visible = True
                self.back.disabled = False

                self.replay.on_click = self.threadReplay
                self.replay.visible = True
                self.replay.disabled = False

    def nextMove(self):
        if not self.rotating:
            # Disable buttons whilst rotating
            self.start.on_click = None
            self.next.on_click = None
            self.back.on_click = None
            move = self.solution[self.moveIndex]
            if move != 'END':
                sleep(.2)
                for _ in range(move[2]):
                    self.rotateFace(move[0], move[1])
                    sleep(.3)

                self.moveIndex += 1
                self.updateMoveCount()

                # Re-enable buttons
                if self.moveIndex == len(self.solution) - 1:
                    self.done.on_click = self.returnToMenu
                    self.done.visible = True
                    self.done.disabled = False
                    self.done.z = 0
                    
                    self.next.on_click = None
                    self.next.visible = False
                    self.next.disabled = True
                    self.next.z = 1

                    self.back.on_click = self.threadPrev
                    self.back.visible = True
                    self.back.disabled = False

                    self.replay.on_click = self.threadReplay
                    self.replay.visible = True
                    self.replay.disabled = False

                    self.start.on_click = None
                    self.start.z = 1
                    self.start.visible = False
                    self.start.disabled = True

                elif self.moveIndex >= 1:
                    self.start.on_click = None
                    self.start.z = 1
                    self.start.visible = False
                    self.start.disabled = True

                    self.next.on_click = self.threadNext
                    self.next.visible = True
                    self.next.disabled = False
                    self.next.z = 0

                    self.back.on_click = self.threadPrev
                    self.back.visible = True
                    self.back.disabled = False

                    self.replay.on_click = self.threadReplay
                    self.replay.visible = True
                    self.replay.disabled = False

    def prevMove(self):
        if not self.rotating:
            # Disable buttons whilst rotating
            self.start.on_click = None
            self.next.on_click = None
            self.back.on_click = None
            move = self.solution[self.moveIndex-1]
            sleep(.2)
            for _ in range(move[2]):
                self.rotateFace(move[0], -move[1])
                sleep(.3)
            
            self.moveIndex -= 1
            self.updateMoveCount()

            if self.moveIndex >= 1:
                self.start.on_click = None
                self.start.z = 1
                self.start.visible = False
                self.start.disabled = True

                self.next.on_click = self.threadNext
                self.next.visible = True
                self.next.disabled = False
                self.next.z = 0

                self.back.on_click = self.threadPrev
                self.back.visible = True
                self.back.disabled = False

                self.replay.on_click = self.threadReplay
                self.replay.visible = True
                self.replay.disabled = False

                self.done.on_click = None
                self.done.visible = False
                self.done.disabled = True
                self.done.z = 1

            elif self.moveIndex == 0:
                self.start.on_click = self.threadNext
                self.start.z = 0
                self.start.visible = True
                self.start.disabled = False

                self.next.on_click = None
                self.next.visible = False
                self.next.disabled = True
                self.next.z = 1

                self.back.on_click = None
                self.back.visible = False
                self.back.disabled = True

                self.replay.on_click = None
                self.replay.visible = False
                self.replay.disabled = True

                self.done.on_click = None
                self.done.visible = False
                self.done.disabled = True
                self.done.z = 1

    def returnToMenu(self):
        self.exitCode.append("M")
        self.destroySelf()
    
    def destroyButtons(self):
        destroy(self.start)
        destroy(self.next)
        destroy(self.back)
        destroy(self.replay)
        destroy(self.done)
    
    def destroyText(self):
        for letter in self.moveCount:
            destroy(letter)
        destroy(self.slash)

    def destroySelf(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    destroy(self.cube[i][j][k])
        
        try:
            self.destroyButtons()
        except:
            print("Buttons not yet created")
        
        try:
            self.destroyText()
        except:
            print("Text not yet created")

    def Update(self):
        if self.rotating:
            if self.rotating_col == "w+":
                if self.rotation_deg + self.rotationSpeed * time.dt >= 90:
                    self.rotateWhite(90-self.rotation_deg)
                    self.reIndexWhite(1)
                    self.disableRotation()
                    self.resetRotationDeg()
                else:
                    self.rotateWhite(self.rotationSpeed * time.dt)
                    self.editRotationDeg(self.rotationSpeed * time.dt)
            elif self.rotating_col == "w-":
                if self.rotation_deg + self.rotationSpeed * time.dt >= 90:
                    self.rotateWhite(self.rotation_deg-90)
                    self.reIndexWhite(-1)
                    self.disableRotation()
                    self.resetRotationDeg()
                else:
                    self.rotateWhite(-self.rotationSpeed * time.dt)
                    self.editRotationDeg(self.rotationSpeed * time.dt)
            elif self.rotating_col == "b+":
                if self.rotation_deg + self.rotationSpeed * time.dt >= 90:
                    self.rotateBlue(90-self.rotation_deg)
                    self.reIndexBlue(1)
                    self.disableRotation()
                    self.resetRotationDeg()
                else:
                    self.rotateBlue(self.rotationSpeed * time.dt)
                    self.editRotationDeg(self.rotationSpeed * time.dt)
            elif self.rotating_col == "b-":
                if self.rotation_deg + self.rotationSpeed * time.dt >= 90:
                    self.rotateBlue(self.rotation_deg-90)
                    self.reIndexBlue(-1)
                    self.disableRotation()
                    self.resetRotationDeg()
                else:
                    self.rotateBlue(-self.rotationSpeed * time.dt)
                    self.editRotationDeg(self.rotationSpeed * time.dt)
            elif self.rotating_col == "r+":
                if self.rotation_deg + self.rotationSpeed * time.dt >= 90:
                    self.rotateRed(90-self.rotation_deg)
                    self.reIndexRed(1)
                    self.disableRotation()
                    self.resetRotationDeg()
                else:
                    self.rotateRed(self.rotationSpeed * time.dt)
                    self.editRotationDeg(self.rotationSpeed * time.dt)
            elif self.rotating_col == "r-":
                if self.rotation_deg + self.rotationSpeed * time.dt >= 90:
                    self.rotateRed(self.rotation_deg-90)
                    self.reIndexRed(-1)
                    self.disableRotation()
                    self.resetRotationDeg()
                else:
                    self.rotateRed(-self.rotationSpeed * time.dt)
                    self.editRotationDeg(self.rotationSpeed * time.dt)
            elif self.rotating_col == "g+":
                if self.rotation_deg + self.rotationSpeed * time.dt >= 90:
                    self.rotateGreen(90-self.rotation_deg)
                    self.reIndexGreen(1)
                    self.disableRotation()
                    self.resetRotationDeg()
                else:
                    self.rotateGreen(self.rotationSpeed * time.dt)
                    self.editRotationDeg(self.rotationSpeed * time.dt)
            elif self.rotating_col == "g-":
                if self.rotation_deg + self.rotationSpeed * time.dt >= 90:
                    self.rotateGreen(self.rotation_deg-90)
                    self.reIndexGreen(-1)
                    self.disableRotation()
                    self.resetRotationDeg()
                else:
                    self.rotateGreen(-self.rotationSpeed * time.dt)
                    self.editRotationDeg(self.rotationSpeed * time.dt)
            elif self.rotating_col == "y+":
                if self.rotation_deg + self.rotationSpeed * time.dt >= 90:
                    self.rotateYellow(90-self.rotation_deg)
                    self.reIndexYellow(1)
                    self.disableRotation()
                    self.resetRotationDeg()
                else:
                    self.rotateYellow(self.rotationSpeed * time.dt)
                    self.editRotationDeg(self.rotationSpeed * time.dt)
            elif self.rotating_col == "y-":
                if self.rotation_deg + self.rotationSpeed * time.dt >= 90:
                    self.rotateYellow(self.rotation_deg-90)
                    self.reIndexYellow(-1)
                    self.disableRotation()
                    self.resetRotationDeg()
                else:
                    self.rotateYellow(-self.rotationSpeed * time.dt)
                    self.editRotationDeg(self.rotationSpeed * time.dt)
            elif self.rotating_col == "o+":
                if self.rotation_deg + self.rotationSpeed * time.dt >= 90:
                    self.rotateOrange(90-self.rotation_deg)
                    self.reIndexOrange(1)
                    self.disableRotation()
                    self.resetRotationDeg()
                else:
                    self.rotateOrange(self.rotationSpeed * time.dt)
                    self.editRotationDeg(self.rotationSpeed * time.dt)
            elif self.rotating_col == "o-":
                if self.rotation_deg + self.rotationSpeed * time.dt >= 90:
                    self.rotateOrange(self.rotation_deg-90)
                    self.reIndexOrange(-1)
                    self.disableRotation()
                    self.resetRotationDeg()
                else:
                    self.rotateOrange(-self.rotationSpeed * time.dt)
                    self.editRotationDeg(self.rotationSpeed * time.dt)
        