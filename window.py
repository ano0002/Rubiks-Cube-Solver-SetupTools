from ursina import *
from thistlethwaite import *
from cube import *
from GUICube import *
from InputMenu import *
from threading import Thread
from solutionTools import SolverTools

app = Ursina(development_mode=True, show_ursina_splash=False)

colourMappings = {
    0 : color.white,
    1 : color.red,
    2 : color.blue,
    3 : color.orange,
    4 : color.green,
    5 : color.yellow
}
            
guiCube = GUICube()
solution = []

def update():
    global guiCube
    global solution
    try:
        if solution[-1] == 'END':
            print("SOLUTION RECEIVED")
            t = Thread(target=guiCube.scrambleToSolution, args=[copy(solution)])
            t.daemon = True
            t.start()
            solution = []
    except:
        pass

    guiCube.Update()

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
    elif key == "l":
        i.destroySelf()


camera.x = 20
camera.y = 20
camera.fov = 25
camera.look_at((0, 0, 0))

i = InputMenu(solution)

app.run()