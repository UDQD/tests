import random
size_x = 8
size_y = 8
map = []
empty =[]
for i in range(size_x):
    for j in range(size_y):
        empty.append((i,j))
for i in range(size_x):
    map.append([None] * size_y)

for i in range(size_x):
    for j in range(size_y):
        map[i][j] = [None]

def rand_coord():
    coord = random.choice(empty)
    empty.remove(coord)
    return coord
def out():
    for e in map:
        print (e);
def add_el(obj,x, y):
    if None in map[obj.x][obj.y]:
        map[obj.x][obj.y].append(obj.tag)
        map[obj.x][obj.y].remove(None)
    else:
        map[obj.x][obj.y].append(obj.tag)
