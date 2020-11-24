import location as loc
class Player:
    tag = 'play'
    def __init__(self, pos_x, pos_y, spawn_x, spawn_y):
        self.x = pos_x
        self.y = pos_y
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.gran = 3

    def death(self):
        self.gran = 3
        self.x = self.spawn_x
        self.y = self.spawn_y

    def action(self, x):
        if 1<=x<=4:
            if x == 1:
                pass
            if x == 2:
                pass
            if x == 3:
                pass
            if x == 4:
                pass
        elif x == 5:
            if x == 1:
                pass
            if x == 2:
                pass
            if x == 3:
                pass
            if x == 4:
                pass


