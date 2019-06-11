import os
import json
import datetime

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

    def __init__(self, config: Config):
        self.config = config
        self.level = Level(config.level_size)
        self.score = 0
        self.speed = 0
        self.snake = None
        self.food = None

    @property
    def actual_bonus(self):
        return max(
            (self.config.points['max_multiplier'] - self.snake.hunger_meter) * self.config.points['hunger_bonus_base'],
            0)

    def setup(self):
        self.level.objects.append(self.snake)
        self.level.objects.append(self.food)

    def start(self):
        self.score = 0
        self.speed = self.config.game_speed
        self.level.clear_objects()
        self.snake = Snake(self.config.snake_size, *self.config.snake_pos, self.config.DIRS)
        self.food = Food(*generate_random_pos(1, self.level.size - 1,
                                              avoid=[(part.x, part.y) for part in self.snake.tail.body]))
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
            self.speed -= self.config.speed_delta
            self.snake.food_eaten = True
            self.food.update_pos(
                *generate_random_pos(1, self.level.size - 1, avoid=[(part.x, part.y) for part in self.snake.tail.body]))

    def add_points(self):
        # Normalizing the multiplier value to 0 if negative
        multiplier = max(self.config.points['max_multiplier'] - self.snake.hunger_meter, 0)
        self.score += self.config.points['food'] + (self.config.points['hunger_bonus_base'] * multiplier)

    def check_highscore(self):
        if not os.path.exists('./highscores.json'):
            return True
        with open('./highscores.json') as f:
            scores = json.load(f)
            if len(scores) < 10:
                return True
            else:
                return scores[-1]['score'] < self.score

    def save_score(self, name):
        file = './highscores.json'
        full_score = {
            'name': name.decode('utf-8'),
            'score': self.score,
            'length': self.snake.size,
            'config': self.config.name,
            'date': str(datetime.datetime.now())
        }
        if os.path.exists(file):
            with open(file, 'r') as f:
                scores = json.load(f)
            added = False
            for i, score in enumerate(scores):
                if score['score'] < self.score:
                    scores.insert(i, full_score)
                    added = True
                    break
            if not added:
                scores.append(full_score)
            while len(scores) > 10:
                scores.pop()
        else:
            scores = [full_score]

        with open(file, 'w') as f:
            json.dump(scores, f)

    def get_highscores(self):
        if not os.path.exists('./highscores.json'):
            return []
        with open('./highscores.json') as f:
            try:
                scores = json.load(f)
            except json.JSONDecodeError:
                scores = []
        return scores
