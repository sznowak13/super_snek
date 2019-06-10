from random import randrange

from level import Level
from snake import Snake, SnakeException
from tiles import Food, Wall
from config import Config


def generate_random_pos(start, stop, avoid=None):
    if avoid:
        pos = randrange(start, stop), randrange(start, stop)
        while pos in avoid:
            pos = randrange(start, stop), randrange(start, stop)
        return pos
    else:
        return randrange(start, stop), randrange(start, stop)


class Game:

    MAX_MULTIPLIER = 50
    FOOD_POINTS = 500
    HUNGER_BONUS_BASE = 100

    def __init__(self, config: Config):
        self.config = config
        self.level = Level(config.level_size)
        self.snake = Snake(config.snake_size, *config.snake_pos, config.DIRS)
        self.food = Food(*generate_random_pos(1, self.level.size - 1,
                                              avoid=[(part.x, part.y) for part in self.snake.tail.body]))
        self.points = 0
        self.speed = config.game_speed

    @property
    def actual_bonus(self):
        return max((self.MAX_MULTIPLIER - self.snake.hunger_meter) * self.HUNGER_BONUS_BASE, 0)

    def setup(self):
        self.level.objects.append(self.snake)
        self.level.objects.append(self.food)

    def restart(self):
        self.points = 0
        self.speed = self.config.game_speed
        self.level.clear_objects()
        self.snake = Snake(self.config.snake_size, *self.config.snake_pos, self.config.DIRS)
        self.food = Food(2, 2)
        self.setup()

    def process_move(self):
        self.snake.move()
        self.check_self_bite()
        self.check_wall_collision()
        self.was_food_eaten()

    def check_self_bite(self):
        for part in self.snake.tail.body:
            if self.snake.head.x == part.x and self.snake.head.y == part.y:
                raise SnakeException("Snake bit itself!")

    def check_wall_collision(self):
        # We are transforming 2d coordinates to 1d coordinate with formula x + y * size
        if isinstance(self.level.tiles[self.snake.x + self.snake.y * self.level.size], Wall):
            raise SnakeException("Snake just tried to eat a wall...")

    def was_food_eaten(self):
        if self.food.x == self.snake.x and self.food.y == self.snake.y:
            self.add_points()
            self.speed -= 500
            self.snake.food_eaten = True
            self.food.update_pos(
                *generate_random_pos(1, self.level.size - 1, avoid=[(part.x, part.y) for part in self.snake.tail.body]))

    def add_points(self):
        # Normalizing the multiplier value to 0 if negative
        multiplier = max(self.MAX_MULTIPLIER - self.snake.hunger_meter, 0)
        self.points += self.FOOD_POINTS + (self.HUNGER_BONUS_BASE * multiplier)
