from tiles import Wall, Floor


class Level:
    def __init__(self, size):
        self.size = size
        self.tiles = [self.generate_tile(x, y) for x in range(self.size) for y in range(self.size)]
        self.objects = []

    def generate_tile(self, x, y):
        borders = (0, self.size - 1)
        if y in borders or x in borders:
            return Wall(x, y)
        else:
            return Floor(x, y)

    def clear_objects(self):
        self.objects = []
