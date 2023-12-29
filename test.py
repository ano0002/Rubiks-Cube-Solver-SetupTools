cube = [[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[10, 11, 12], [13, 14, 15], [16, 17, 18]], 
        [[19, 20, 21], [22, 23, 24], [25, 26, 27]]]

print(cube)
print(cube[0][1][1])

cube[0] = list(list(x) for x in zip(*cube[0]))
cube[1] = list(list(x) for x in zip(*cube[1]))
cube[2] = list(list(x) for x in zip(*cube[2]))
cube = list(list(x) for x in zip(*cube))

print(cube)

# cube[2] = list(list(x) for x in zip(*cube[2]))[::-1]
# print(cube)

cube = list(list(x) for x in zip(*cube))
cube[0] = list(list(x) for x in zip(*cube[0]))
cube[1] = list(list(x) for x in zip(*cube[1]))
cube[2] = list(list(x) for x in zip(*cube[2]))

print(cube)