import curses


class ConsoleDisplay:
    USER_COMMANDS = {
        ord('q'): "QUIT",
        ord('o'): "OPTIONS",
        ord('s'): "START"
    }

    def __init__(self, win, lvl_size):
        self.win = win
        self.setup_curses()
        self.maxyx = win.getmaxyx()
        # offset's x coordinate is modified for better visual experience
        self.offset = ((self.maxyx[0] - lvl_size) // 2, (self.maxyx[1] - lvl_size * 2) // 2)

    def setup_curses(self):
        curses.start_color()
        curses.use_default_colors()
        for i in range(curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        curses.noecho()
        curses.curs_set(0)

    def start_game_display(self):
        self.win.nodelay(True)

    def stop_game_display(self):
        self.win.nodelay(False)

    def get_user_input(self, dirs=None):
        if dirs is None:
            dirs = {}
        inpt = self.win.getch()
        if inpt in self.USER_COMMANDS:
            return self.USER_COMMANDS[inpt]
        elif dirs:
            return self.get_dir(inpt, dirs)

    def get_dir(self, move, dirs):
        if move == curses.KEY_UP:
            return dirs['UP']
        elif move == curses.KEY_RIGHT:
            return dirs['RIGHT']
        elif move == curses.KEY_DOWN:
            return dirs['DOWN']
        elif move == curses.KEY_LEFT:
            return dirs['LEFT']

    def display_stats(self, game):
        length_display = "LENGTH: {}".format(len(game.snake.tail))
        bonus_display = "BONUS: {}".format(game.actual_bonus)
        length_display_x_origin = self.offset[1] + game.level.size * 2 - len(length_display) - 1
        bonus_display_x_origin = self.offset[1] + game.level.size
        self.win.move(self.offset[0] - 1, self.offset[1])
        self.win.clrtoeol()
        self.win.addstr(self.offset[0] - 1, self.offset[1], "POINTS: " + str(game.points))
        self.win.addstr(self.offset[0] - 1, length_display_x_origin, length_display)
        self.win.addstr(self.offset[0] - 1, bonus_display_x_origin, bonus_display)

    def display_gameboard(self, game):
        for tile in game.level.tiles:
            color = game.config.get_color(tile.name)
            self.win.addstr(tile.y + self.offset[0], tile.x * 2 + self.offset[1], tile.ch, curses.color_pair(color))

        for obj in game.level.objects:
            draw_data = obj.get_drawing_data()
            for data in draw_data:
                color = game.config.get_color(data.name)
                self.win.addstr(data.y + self.offset[0], data.x * 2 + self.offset[1], data.ch, curses.color_pair(color))

    def display_gameover(self, game, err):
        curses.cbreak()
        self.win.nodelay(False)
        self.win.addstr(self.offset[0] - 3, self.offset[1], "GAME OVER: " + str(err), curses.color_pair(game.config.get_color("ERR")))
        self.win.addstr(self.offset[0] - 2, self.offset[1], "Press 'q' to quit or 'r' to restart",
                   curses.color_pair(game.config.get_color("INFO")))

        while True:
            cmd = self.win.getch()
            if cmd == ord('q'):
                return 'QUIT'
            elif cmd == ord('r'):
                self.win.clear()
                self.win.nodelay(True)
                return 'RESTART'
