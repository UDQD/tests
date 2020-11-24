import random

size_x = 8
size_y = 8
mape = []
tags = []
empty = []
win = False
for i in range(size_x):
    for j in range(size_y):
        empty.append((i, j))
for i in range(size_x):
    tags.append(['    '] * size_y)
    mape.append([None] * size_y)

for i in range(size_x):
    for j in range(size_y):
        tags[i][j] = ['    ']
        mape[i][j] = [None]


def rand_coord():
    coord = random.choice(empty)
    empty.remove(coord)
    return coord


def out():
    for e in tags:
        print(e);


def add_el(obj, x, y):
    if None in mape[obj.x][obj.y]:
        mape[obj.x][obj.y].append(obj)
        mape[obj.x][obj.y].remove(None)

        tags[obj.x][obj.y].append(obj.tag)
        tags[obj.x][obj.y].remove('    ')
    else:
        mape[obj.x][obj.y].append(obj)
        tags[obj.x][obj.y].append(obj.tag)


def step(player, x, y):
    if 'wall' in tags[x][y] or x > 7 or y > 7 or x < 0 or y < 0:
        print("Тут стена, пройти нельзя")
    else:
        player.x = x
        player.y = y
        if 'zomb' in tags[x][y]:
            if mape[x][y][0].is_alive:
                print("На вас напал зомби")
                player.death()
            else:
                print("Вы нашли мертвого зомби")
            if 'key_' in tags[x][y]:
                mape[x][y][tags[x][y].index('key_')].on_player = True
            if 'door' in tags[x][y]:
                print("Вы нашли дверь")
                if 'key_' in tags[x][y]:
                    print("Дверь открыта. ПОБЕДА")
                    win = True


