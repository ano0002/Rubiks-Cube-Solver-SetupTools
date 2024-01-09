import pickle
import math
import queue
import random
from cube import *


def IDAStar(cube: Cube, goal: Cube, heuristic: dict, max_depth: int=20):
    distance = IDAStarRecursion(cube, goal, heuristic, max_depth, 0)
    if distance <= 0:
        print("Found at depth", -distance)
    else:
        print("Not found")

def IDAStarRecursion(cube: Cube, goal: Cube, heuristic: dict, max_depth: int, depth: int) -> int:
    if cube.getState() == goal.getState():
        # Goal reached
        print("Found")
        return -depth
    
    try:
        estimate = depth + heuristic[cube.getCornerCode()]
    except:
        estimate = depth + 11

    if estimate > max_depth:
        print("Breached max_depth. Est:", estimate)
        return estimate
    
    min = math.inf
    for i in range(2):
        for j in range(6):
            newCube = Cube(state=cube.getState())
            if i == 0:
                newCube.rotateFace(j, 1)
            else:
                newCube.rotateFace(j, -1)
            v = IDAStarRecursion(newCube, goal, heuristic, max_depth, depth+1)
            if v < 0:
                return v
            elif v < min:
                min = v
    
    return min

cube = getRandomScramble(1)
goal = Cube()

with open(r"cornerDB.pickle", "rb") as f:
    db = pickle.load(f)

IDAStar(cube, goal, db, 1)
