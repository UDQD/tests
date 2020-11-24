import location as loc
import zombie
import walls
import player
import spawn
import key
import door
# for i in range(10):
#     print(loc.rand_coord())

for i in range(15):
    walls.Walls(*loc.rand_coord())

for i in range(15):
    zombie.Zombie(*loc.rand_coord())
    # walls.append(new_wall)

obj_spawn = spawn.Spawn(*loc.rand_coord())

player.Player(*loc.rand_coord(), obj_spawn.x, obj_spawn.y)

key.Key(*loc.rand_coord())

door.Door(*loc.rand_coord())


loc.out()
# while(not loc.win):
#     pass
# loc.map[5][5].append('afeafa')
# print('\n')
# loc.out()
# print(loc.map[5][5])