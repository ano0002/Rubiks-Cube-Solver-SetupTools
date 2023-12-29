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

def input(key):
    if key == 'w':
        rotateYellow(1)
    elif key == 's':
        rotateYellow(-1)
    elif key == 'a':
        rotateBlue(1)
    elif key == 'd':
        rotateBlue(-1)
    elif key == 'e':
        rotateWhite(1)
    elif key == 'q':
        rotateWhite(-1)
    elif key == 'j':
        rotateGreen(1)
    elif key == 'l':
        rotateGreen(-1)
    elif key == 'i':
        rotateOrange(1)
    elif key == 'k':
        rotateOrange(-1)
    elif key == 'u':
        rotateRed(1)
    elif key == 'o':
        rotateRed(-1)
    elif key == "up arrow":
        cube[1][1][1].rotation_x += 45
    elif key == "down arrow":
        cube[1][1][1].rotation_x -= 45
    elif key == "left arrow":
        cube[1][1][1].rotation_y += 45
    elif key == "right arrow":
        cube[1][1][1].rotation_y -= 45

def rotateYellow(scale: int):
    global cube
    for line in cube[0]:
        for piece in line:
            if piece != cube[0][1][1]:
                piece.world_parent = cube[0][1][1]
    cube[0][1][1].rotation_x += scale * 90
    for line in cube[0]:
        for piece in line:
            piece.world_parent = cube[1][1][1]

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
    cube[2][1][1].rotation_x += scale * 90
    for line in cube[2]:
        for piece in line:
            piece.world_parent = cube[1][1][1]

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
    cube[1][1][0].rotation_z -= scale * 90
    for i in range(3):
        for k in range(3):
            cube[i][k][0].world_parent = cube[1][1][1]
    
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
    cube[1][1][2].rotation_z -= scale * 90
    for i in range(3):
        for k in range(3):
            cube[i][k][2].world_parent = cube[1][1][1]
    
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
    cube[1][0][1].rotation_y += scale * 90
    for i in range(3):
        for k in range(3):
            cube[i][0][k].world_parent = cube[1][1][1]
    
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
    cube[1][2][1].rotation_y += scale * 90
    for i in range(3):
        for k in range(3):
            cube[i][2][k].world_parent = cube[1][1][1]
    
    #make cube[2] the red face
    cube = list(list(x) for x in zip(*cube)) 

    #rotate as usual
    if scale < 0:
        cube[2] = list(list(x) for x in zip(*cube[2]))[::-1]
    else:
        cube[2] = list(list(x) for x in zip(*(cube[2][::-1])))
    
    #revert
    cube = list(list(x) for x in zip(*cube)) 
    
#smooth rotations check
    #does this shit work?

app.run()