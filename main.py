import curses

from config import Config
from game import Game
from snake import SnakeException
from display import ConsoleDisplay


def start_game(game: Game, display: ConsoleDisplay):
    game.start()
    display.start_game_display()

    frame = 0
    running = True
    direction = None
    while running:
        user_input = display.get_user_input(game.config.DIRS)

        if user_input in game.config.DIRS.values():
            direction = user_input
        else:
            if user_input == 'QUIT':
                running = False

        if not frame % game.speed:
            if direction is not None:
                game.snake.dir = direction
                direction = None

            frame = 0
            display.display_stats(game)
            display.display_gameboard(game)

            try:
                game.process_move()
            except SnakeException as e:
                display.stop_game_display()
                display.display_gameover(game, e)

                if game.check_highscore():
                    score_name = display.ask_highscore_input(game.level.size)
                    game.save_score(score_name)
                    display.clear_game_board()
                    break

                game_over = True
                while game_over:
                    game_over = False
                    cmd = display.get_user_input()

                    if cmd == 'QUIT':
                        running = False
                    elif cmd == 'START':
                        game.start()
                        display.start_game_display()
                    else:
                        game_over = True
        frame += 1


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
            display.clear_game_board()
            start_game(game, display)
        elif cmd == "OPTIONS":
            display.show_options()
        elif cmd == "QUIT":
            app_running = False


if __name__ == '__main__':
    curses.wrapper(main)
