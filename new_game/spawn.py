import location as loc
class Spawn:
    tag = 'spaw'
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        loc.add_el(self, self.x, self.y)