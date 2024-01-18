from ursina import *
from thistlethwaite import *
from cube import *
from GUICube import *
from InputMenu import *
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
            
guiCube = GUICube()

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