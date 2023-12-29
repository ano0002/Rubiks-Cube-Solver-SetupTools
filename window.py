from ursina import *

app = Ursina()

cubepiece = Entity(model='cube', color=color.black)
blueplate = Entity(model="cube", scale_x=0.9, scale_y=0.9, scale_z=0.1, z=-0.5, color=color.blue, parent=cubepiece)
yellowplate = Entity(model="cube", scale_x=0.1, scale_y=0.9, scale_z=0.9, x=-0.5, color=color.yellow, parent=cubepiece)
redplate = Entity(model="cube", scale_x=0.9, scale_y=0.1, scale_z=0.9, y=0.5, color=color.red, parent=cubepiece)
whiteplate = Entity(model="cube", scale_x=0.1, scale_y=0.9, scale_z=0.9, x=0.5, color=color.white, parent=cubepiece)
orangeplate = Entity(model="cube", scale_x=0.9, scale_y=0.1, scale_z=0.9, y=-0.5, color=color.orange, parent=cubepiece)
greenplate = Entity(model="cube", scale_x=0.9, scale_y=0.9, scale_z=0.1, z=0.5, color=color.green, parent=cubepiece)

cube = []
for i in range(3):
    layer = []
    for j in range(3):
        line = []
        for k in range(3):
            piece = duplicate(cubepiece)
            piece.set_position((i-1, j-1, k-1))
            line.append(piece)
        layer.append(line)
    cube.append(layer)

destroy(cubepiece)


for layer in cube:
    for line in layer:
        for piece in line:
            if piece != cube[1][1][1]:
                piece.world_parent = cube[1][1][1]

camera.x = 20
camera.y = 20
camera.fov = 30
camera.look_at((0, 0, 0))

rotating = False
rotating_col = None
ROTATION_SPEED = 200
rotation_deg = 0

def update():
    global rotating
    global rotating_col
    global rotation_deg
    if rotating:
        if rotating_col == "w+":
            if rotation_deg + ROTATION_SPEED * time.dt >= 90:
                rotateWhite(90-rotation_deg)
                reIndexWhite(1)
                rotating = False
                rotation_deg = 0
            else:
                rotateWhite(ROTATION_SPEED * time.dt)
                rotation_deg += ROTATION_SPEED * time.dt
        elif rotating_col == "w-":
            if rotation_deg + ROTATION_SPEED * time.dt >= 90:
                rotateWhite(rotation_deg-90)
                reIndexWhite(-1)
                rotating = False
                rotation_deg = 0
            else:
                rotateWhite(-ROTATION_SPEED * time.dt)
                rotation_deg += ROTATION_SPEED * time.dt
        elif rotating_col == "b+":
            if rotation_deg + ROTATION_SPEED * time.dt >= 90:
                rotateBlue(90-rotation_deg)
                reIndexBlue(1)
                rotating = False
                rotation_deg = 0
            else:
                rotateBlue(ROTATION_SPEED * time.dt)
                rotation_deg += ROTATION_SPEED * time.dt
        elif rotating_col == "b-":
            if rotation_deg + ROTATION_SPEED * time.dt >= 90:
                rotateBlue(rotation_deg-90)
                reIndexBlue(-1)
                rotating = False
                rotation_deg = 0
            else:
                rotateBlue(-ROTATION_SPEED * time.dt)
                rotation_deg += ROTATION_SPEED * time.dt
        elif rotating_col == "r+":
            if rotation_deg + ROTATION_SPEED * time.dt >= 90:
                rotateRed(90-rotation_deg)
                reIndexRed(1)
                rotating = False
                rotation_deg = 0
            else:
                rotateRed(ROTATION_SPEED * time.dt)
                rotation_deg += ROTATION_SPEED * time.dt
        elif rotating_col == "r-":
            if rotation_deg + ROTATION_SPEED * time.dt >= 90:
                rotateRed(rotation_deg-90)
                reIndexRed(-1)
                rotating = False
                rotation_deg = 0
            else:
                rotateRed(-ROTATION_SPEED * time.dt)
                rotation_deg += ROTATION_SPEED * time.dt
        elif rotating_col == "g+":
            if rotation_deg + ROTATION_SPEED * time.dt >= 90:
                rotateGreen(90-rotation_deg)
                reIndexGreen(1)
                rotating = False
                rotation_deg = 0
            else:
                rotateGreen(ROTATION_SPEED * time.dt)
                rotation_deg += ROTATION_SPEED * time.dt
        elif rotating_col == "g-":
            if rotation_deg + ROTATION_SPEED * time.dt >= 90:
                rotateGreen(rotation_deg-90)
                reIndexGreen(-1)
                rotating = False
                rotation_deg = 0
            else:
                rotateGreen(-ROTATION_SPEED * time.dt)
                rotation_deg += ROTATION_SPEED * time.dt
        elif rotating_col == "y+":
            if rotation_deg + ROTATION_SPEED * time.dt >= 90:
                rotateYellow(90-rotation_deg)
                reIndexYellow(1)
                rotating = False
                rotation_deg = 0
            else:
                rotateYellow(ROTATION_SPEED * time.dt)
                rotation_deg += ROTATION_SPEED * time.dt
        elif rotating_col == "y-":
            if rotation_deg + ROTATION_SPEED * time.dt >= 90:
                rotateYellow(rotation_deg-90)
                reIndexYellow(-1)
                rotating = False
                rotation_deg = 0
            else:
                rotateYellow(-ROTATION_SPEED * time.dt)
                rotation_deg += ROTATION_SPEED * time.dt
        elif rotating_col == "o+":
            if rotation_deg + ROTATION_SPEED * time.dt >= 90:
                rotateOrange(90-rotation_deg)
                reIndexOrange(1)
                rotating = False
                rotation_deg = 0
            else:
                rotateOrange(ROTATION_SPEED * time.dt)
                rotation_deg += ROTATION_SPEED * time.dt
        elif rotating_col == "o-":
            if rotation_deg + ROTATION_SPEED * time.dt >= 90:
                rotateOrange(rotation_deg-90)
                reIndexOrange(-1)
                rotating = False
                rotation_deg = 0
            else:
                rotateOrange(-ROTATION_SPEED * time.dt)
                rotation_deg += ROTATION_SPEED * time.dt

def input(key):
    global rotating
    global rotating_col
    if key == "up arrow":
        cube[1][1][1].rotation_x += 45
    elif key == "down arrow":
        cube[1][1][1].rotation_x -= 45
    elif key == "left arrow":
        cube[1][1][1].rotation_y += 45
    elif key == "right arrow":
        cube[1][1][1].rotation_y -= 45
    elif key == "w":
        if not rotating:
            rotating_col = "w+"
            rotating = True
    elif key == "s":
        if not rotating:
            rotating_col = "w-"
            rotating = True
    elif key == "r":
        if not rotating:
            rotating_col = "r+"
            rotating = True
    elif key == "f":
        if not rotating:
            rotating_col = "r-"
            rotating = True
    elif key == "t":
        if not rotating:
            rotating_col = "b+"
            rotating = True
    elif key == "g":
        if not rotating:
            rotating_col = "b-"
            rotating = True
    elif key == "e":
        if not rotating:
            rotating_col = "g+"
            rotating = True
    elif key == "d":
        if not rotating:
            rotating_col = "g-"
            rotating = True
    elif key == "y":
        if not rotating:
            rotating_col = "y+"
            rotating = True
    elif key == "h":
        if not rotating:
            rotating_col = "y-"
            rotating = True
    elif key == "u":
        if not rotating:
            rotating_col = "o+"
            rotating = True
    elif key == "j":
        if not rotating:
            rotating_col = "o-"
            rotating = True

def rotateYellow(scale: int):
    global cube
    for line in cube[0]:
        for piece in line:
            if piece != cube[0][1][1]:
                piece.world_parent = cube[0][1][1]
    cube[0][1][1].rotation_x += scale * 1
    for line in cube[0]:
        for piece in line:
            piece.world_parent = cube[1][1][1]

def reIndexYellow(scale: int):
    global cube
    #rearrange cube indices
    #Anti-clockwise -> transpose then reverse
    #Clockwise -> reverse then transpose
    if scale > 0:
        cube[0] = list(list(x) for x in zip(*cube[0]))[::-1]
    else:
        cube[0] = list(list(x) for x in zip(*(cube[0][::-1])))

def rotateWhite(scale: int):
    global cube
    for line in cube[2]:
        for piece in line:
            if piece != cube[2][1][1]:
                piece.world_parent = cube[2][1][1]
    cube[2][1][1].rotation_x += scale * 1
    for line in cube[2]:
        for piece in line:
            piece.world_parent = cube[1][1][1]

def reIndexWhite(scale: int):
    global cube
    #rearrange cube indices
    #Anti-clockwise -> transpose then reverse
    #Clockwise -> reverse then transpose
    if scale > 0:
        cube[2] = list(list(x) for x in zip(*cube[2]))[::-1]
    else:
        cube[2] = list(list(x) for x in zip(*(cube[2][::-1])))

def rotateBlue(scale: int):
    global cube
    for i in range(3):
        for k in range(3):
            if i != 1 or k != 1:
                cube[i][k][0].world_parent = cube[1][1][0]
    cube[1][1][0].rotation_z -= scale * 1
    for i in range(3):
        for k in range(3):
            cube[i][k][0].world_parent = cube[1][1][1]
    
def reIndexBlue(scale: int):
    global cube
    # make cube[0] the blue face
    cube[0] = list(list(x) for x in zip(*cube[0]))
    cube[1] = list(list(x) for x in zip(*cube[1]))
    cube[2] = list(list(x) for x in zip(*cube[2]))
    cube = list(list(x) for x in zip(*cube)) 

    #rearrange cube indices, rotations as before
    if scale > 0:
        cube[0] = list(list(x) for x in zip(*cube[0]))[::-1]
    else:
        cube[0] = list(list(x) for x in zip(*(cube[0][::-1])))
    
    # revert to original layout
    cube = list(list(x) for x in zip(*cube)) 
    cube[0] = list(list(x) for x in zip(*cube[0]))
    cube[1] = list(list(x) for x in zip(*cube[1]))
    cube[2] = list(list(x) for x in zip(*cube[2]))

def rotateGreen(scale: int):
    global cube
    for i in range(3):
        for k in range(3):
            if i != 1 or k != 1:
                cube[i][k][2].world_parent = cube[1][1][2]
    cube[1][1][2].rotation_z -= scale * 1
    for i in range(3):
        for k in range(3):
            cube[i][k][2].world_parent = cube[1][1][1]
    
def reIndexGreen(scale: int):
    global cube
    # make cube[2] the green face
    cube[0] = list(list(x) for x in zip(*cube[0]))
    cube[1] = list(list(x) for x in zip(*cube[1]))
    cube[2] = list(list(x) for x in zip(*cube[2]))
    cube = list(list(x) for x in zip(*cube)) 

    #rearrange cube indices, rotations as before
    if scale > 0:
        cube[2] = list(list(x) for x in zip(*cube[2]))[::-1]
    else:
        cube[2] = list(list(x) for x in zip(*(cube[2][::-1])))
    
    # revert to original layout
    cube = list(list(x) for x in zip(*cube)) 
    cube[0] = list(list(x) for x in zip(*cube[0]))
    cube[1] = list(list(x) for x in zip(*cube[1]))
    cube[2] = list(list(x) for x in zip(*cube[2]))

def rotateOrange(scale: int):
    global cube
    for i in range(3):
        for k in range(3):
            if i != 1 or k != 1:
                cube[i][0][k].world_parent = cube[1][0][1]
    cube[1][0][1].rotation_y += scale * 1
    for i in range(3):
        for k in range(3):
            cube[i][0][k].world_parent = cube[1][1][1]
    
def reIndexOrange(scale: int):
    global cube
    #make cube[0] the orange face
    cube = list(list(x) for x in zip(*cube)) 

    #rotate as usual
    if scale < 0:
        cube[0] = list(list(x) for x in zip(*cube[0]))[::-1]
    else:
        cube[0] = list(list(x) for x in zip(*(cube[0][::-1])))
    
    #revert
    cube = list(list(x) for x in zip(*cube)) 

def rotateRed(scale: int):
    global cube
    for i in range(3):
        for k in range(3):
            if i != 1 or k != 1:
                cube[i][2][k].world_parent = cube[1][2][1]
    cube[1][2][1].rotation_y += scale * 1
    for i in range(3):
        for k in range(3):
            cube[i][2][k].world_parent = cube[1][1][1]
    
def reIndexRed(scale: int):
    global cube
    #make cube[2] the red face
    cube = list(list(x) for x in zip(*cube)) 

    #rotate as usual
    if scale < 0:
        cube[2] = list(list(x) for x in zip(*cube[2]))[::-1]
    else:
        cube[2] = list(list(x) for x in zip(*(cube[2][::-1])))
    
    #revert
    cube = list(list(x) for x in zip(*cube)) 

app.run()