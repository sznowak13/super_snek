from abc import ABC


class Tile(ABC):
    def __init__(self, x, y, ch, name):
        self.x = x
        self.y = y
        self.ch = ch
        self.name = name

    def get_drawing_data(self):
        return self

    def update_pos(self, x, y):
        self.x = x
        self.y = y


class Floor(Tile):
    def __init__(self, x, y):
        super(Floor, self).__init__(x, y, ' ', 'FLOOR')


class Wall(Tile):
    def __init__(self, x, y):
        super(Wall, self).__init__(x, y, '#', 'WALL')


class Food(Tile):
    def __init__(self, x, y):
        super(Food, self).__init__(x, y, '*', 'FOOD')

    def get_drawing_data(self):
        return self,
