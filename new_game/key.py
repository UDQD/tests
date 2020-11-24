import location as loc
class Key:
    tag = 'key_'
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.on_player = False
        loc.add_el(self,self.x,self.y)