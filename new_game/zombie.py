import location as loc
class Zombie:
    tag = 'zomb'
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.is_alive = True
        loc.add_el(self,self.x,self.y)