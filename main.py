from ursina import *
from thistlethwaite import *
from cube import *
from GUICube import *
from InputMenu import *
from threading import Thread
from MainMenu import *

app = Ursina(development_mode=False, show_ursina_splash=False)

colourMappings = {
    0 : color.white,
    1 : color.red,
    2 : color.blue,
    3 : color.orange,
    4 : color.green,
    5 : color.yellow
}

exitCode = []
guiCube = GUICube(exitCode)
solution = []

# Close Button
close = Button(model='quad', scale=.05, color=color.color(0.7, 0.7, 0.7, 1), x=0.835, y=0.45, z=-5, text="X", on_click=exit)
close.text_entity.size = .05
close.text_entity.font = r"Data\CurvedSquare-eDzl.ttf"

def update():
    global guiCube
    global solution
    global exitCode

    try:
        # Test to see cube hasn't been destroyed, make new one if it has
        guiCube.cube[0][0][0].x
    except:
        # If M has been passed out of the GUICube, it means a menu must be created
        try:
            if exitCode[0] == "M":
                exitCode = []
                guiCube = GUICube(exitCode)
                m = MainMenu(guiCube, solution)
        except:
            guiCube = GUICube(exitCode)

    try:
        if solution[-1] == 'END':
            t = Thread(target=guiCube.scrambleToSolution, args=[copy(solution)])
            t.daemon = True
            t.start()
            solution = []
    except:
        pass

    guiCube.Update()

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
    elif key == "n":
        guiCube.destroySelf()


camera.x = 20
camera.y = 20
camera.fov = 25
camera.look_at((0, 0, 0))

m = MainMenu(guiCube, solution)

app.run()