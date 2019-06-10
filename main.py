import curses

from game import Game, Config
from snake import SnakeException
from display import ConsoleDisplay


def start_game(game, display):
    game.start()
    display.start_game_display()
    frame = 0
    running = True
    while running:
        user_input = display.get_user_input(game.config.DIRS)
        if user_input in game.config.DIRS.values():
            game.snake.dir = user_input
        else:
            if user_input == 'QUIT':
                running = False
            elif user_input == 'OPTIONS':
                pass

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
                    game.start()
        frame += 1
    display.stop_game_display()


def main(win):
    game = Game(Config.from_json('default'))

    display = ConsoleDisplay(win, game.level.size)
    app_running = True
    while app_running:
        display.show_header()
        display.display_gameboard(game)
        display.help_info()
        cmd = display.get_user_input()
        if cmd == "START":
            display.clear_scr()
            start_game(game, display)
        elif cmd == "OPTIONS":
            display.show_options()


if __name__ == '__main__':
    curses.wrapper(main)
