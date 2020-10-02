import location as loc
import zombie
import walls

# for i in range(10):
#     print(loc.rand_coord())

for i in range(3):
    walls.Walls(*loc.rand_coord())
    # walls.append(new_wall)

loc.out()
# loc.map[5][5].append('afeafa')
# print('\n')
# loc.out()
# print(loc.map[5][5])