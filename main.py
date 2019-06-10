import curses

from game import Game, Config
from snake import SnakeException
from display import ConsoleDisplay


def main(win):
    game = Game(Config.from_json('default'))
    game.setup()

    display = ConsoleDisplay(win, game.level.size)

    frame = 0
    running = True
    while running:
        user_input = display.get_user_input(game.config.DIRS)
        if user_input in game.config.DIRS.values():
            game.snake.dir = user_input
        else:
            if user_input == 'QUIT':
                running = False

        if not frame % game.config.game_speed:
            frame = 0
            display.display_stats(game)
            display.display_gameboard(game)

            try:
                game.process_move()
            except SnakeException as e:
                cmd = display.display_gameover(game, e)
                if cmd == 'QUIT':
                    running = False
                elif cmd == 'RESTART':
                    game.restart()
        frame += 1


if __name__ == '__main__':
    curses.wrapper(main)
