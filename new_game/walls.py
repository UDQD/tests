import location as loc
class Walls:
    tag = 'wall'
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y

        # if None in loc.map[self.x][self.y]:
        #     loc.map[self.x][self.y] = "self"
        # else:
        #     loc.map[self.x][self.y].append("self")
        loc.add_el(self,self.x,self.y)
        # Wall.walls.append([self.x,self.y])