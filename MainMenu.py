from ursina import *
from GUICube import GUICube
from time import sleep
from random import randint
from threading import Thread
from InputMenu import *

class MainMenu:
    def __init__(self, guiCube: GUICube, solution: list):
        self.guiCube = guiCube
        self.solution = solution
        self.end = False

        text = "rubiks cube solver"
        y = 0.4
        titletext = dedent(text)

        Text.default_font = r"Data\CurvedSquare-eDzl.ttf"
        Text.default_resolution = 4320 * Text.size

        title = Text(size=.08)
        title.text = titletext
        fullwidth = title.width

        destroy(title)

        self.letters = []
        colors = [color.white, color.red, color.blue, color.orange, color.green, color.yellow]
        col_i = 0
        for i, char in enumerate(text):
            letter = Text(size=.08)
            letter.text = dedent(char)
            letter.x = -fullwidth/2 + i*(fullwidth/len(text))
            letter.y = y
            if char != " ":
                letter.color = colors[col_i]
                col_i += 1
                col_i %= len(colors)
            
            self.letters.append(letter)
        
        self.startButton = Button(model='quad', text=' Start ', visible=True, scale_x=.175, scale_y = 0.075, x=-0.145, y=-0.375, color=color.black90)
        self.instructions = Button(model='quad', text=' Instructions ', visible=True, scale_x=.175, scale_y = 0.075, x=0.145, y=-0.375, color=color.black90)

        self.startButton.text_entity.font = r'Data\DMSans36pt-Regular.ttf'
        self.instructions.text_entity.font = r'Data\DMSans36pt-Regular.ttf'

        self.startButton.on_click = self.start

        t = Thread(target=self.animateCube)
        t.daemon = True
        t.start()

    def destroySelf(self):
        self.end = True
        for letter in self.letters:
            destroy(letter)

        destroy(self.startButton)
        destroy(self.instructions)
        self.guiCube.destroySelf()

    def start(self):
        self.destroySelf()
        i = InputMenu(self.solution)

    def animateCube(self):
        sleep(2)
        while True:
            if self.end:
                break
            if not self.guiCube.rotating:
                try:
                    face = randint(0, 5)
                    dir = randint(0, 1)
                    if dir == 0: dir=-1

                    wait = randint(2,6)
                    wait = wait/2

                    self.guiCube.rotateFace(face, dir)
                    sleep(wait)
                except:
                    break
