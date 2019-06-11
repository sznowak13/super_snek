from tiles import CachedTile


class SnakeException(Exception):
    pass


class SnakeHead(CachedTile):
    def __init__(self, x, y):
        super(SnakeHead, self).__init__(x, y, 'Q', 'SNAKE_HEAD')


class SnakeBody(CachedTile):
    def __init__(self, x, y):
        super(SnakeBody, self).__init__(x, y, 'o', 'SNAKE_BODY')


class SnakeTail:
    def __init__(self, size, head):
        self.origin = head.x - 1
        self.body = [SnakeBody(self.origin - i, head.y) for i in range(size)]

    def follow(self, head: SnakeHead):
        prev = head.prev
        for part in self.body:
            part.cache_prev()
            part.x = prev[0]
            part.y = prev[1]
            prev = part.prev

    def add_part(self):
        last_part = self.body[-1]
        self.body.append(SnakeBody(last_part.prev[0], last_part.prev[1]))

    def __len__(self):
        return len(self.body)


class Snake:
    def __init__(self, size, x, y, dirs):
        self.head = SnakeHead(x, y)
        self.tail = SnakeTail(size, self.head)
        self.dirs = dirs
        self._dir = self.dirs['RIGHT']
        self.food_eaten = False
        self.hunger_meter = 0

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, val):
        # you cant turn back
        if not abs(self._dir - val) == 2:
            self._dir = val

    @property
    def x(self):
        return self.head.x

    @property
    def y(self):
        return self.head.y

    def __len__(self):
        return len(self.tail)

    def get_drawing_data(self):
        return [self.head.get_drawing_data()] + [part for part in self.tail.body]

    def move(self):
        # Digesting food...
        self.hunger_meter += 1
        if self.food_eaten:
            self.tail.add_part()
            self.food_eaten = False
            self.hunger_meter = 0

        dirs = self.dirs
        self.head.cache_prev()
        if self.dir == dirs['UP']:
            self.head.y -= 1
        elif self.dir == dirs['RIGHT']:
            self.head.x += 1
        elif self.dir == dirs['DOWN']:
            self.head.y += 1
        elif self.dir == dirs['LEFT']:
            self.head.x -= 1
        self.tail.follow(self.head)
