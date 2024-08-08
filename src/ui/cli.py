import curses
import sys

from game import BaseGame, Player
from game.base_game import GameStatus


class CliGame(BaseGame):
    # TODO: move settings to config file
    TABLE_LEFT_PAD = 4
    TABLE_TOP_PAD = 1

    # TODO: move to locale dict
    TEXT_GAME_TITLE = "TIC TAC TOE"
    TEXT_DEFAULT_PLAYER_NAME = "Player {}"
    TEXT_USER_TURN = "{}'s turn."
    TEXT_USER_INPUT = "Select cell where to place symbol \"{}\": "
    TEXT_WINNER = "{} is the winner!"
    TEXT_WAIT_KEY = "Press any key to continue... "
    TEXT_CLOSE_GAME = "(Press Ctrl+C to exit)"
    TEXT_PLAY_ERROR = ("Selected cell is invalid, or already occupied by another user.\n"
                       "Please type your preferred cell location like: \"a1\".")
    TEXT_SMALL_DISPLAY = "Terminal window is too small. Please try enlarging it."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._stdscr = None

    def get_user_play(self, player: Player) -> str:
        curses.echo()
        user_play = self._stdscr.getstr(self.TABLE_TOP_PAD + self.board_size[0] * 2 + 2,
                                        len(self.TEXT_USER_INPUT)).decode('utf-8')
        curses.noecho()
        return user_play

    def add_player(self, symbol: str | None = None, name: str | None = None):
        super().add_player(symbol, name or self.TEXT_DEFAULT_PLAYER_NAME.format(self.num_players + 1))

    def reset_preserve_players(self):
        """
        Reset the game preserving players.
        """
        players = self._players
        self.reset()
        self._players = players

    def start(self):
        """
        Start the game.
        """
        curses.wrapper(self._start_wrap)
        self.reset()

    def _start_wrap(self, stdscr):
        """
        Start the game by init screen and request play.

        :param stdscr: Standard screen to display game.
        """
        self._stdscr = stdscr
        self._display_clean()
        self.play()

    def play(self):
        """
        Play the game by taking turns among players.
        """
        while True:
            self._display_clean()
            self._display_board(self.TABLE_TOP_PAD)
            self._display_text(self.TEXT_CLOSE_GAME, self.TABLE_TOP_PAD + self.board_size[0] * 2 + 3)
            if self.status in [GameStatus.READY, GameStatus.ONGOING]:
                self._display_user_turn(self.TABLE_TOP_PAD + self.board_size[0] * 2 + 1)
                try:
                    self.step()
                except ValueError:
                    self._display_error(self.TEXT_PLAY_ERROR, 1)
                    self._display_wait_key(3)
            else:
                self._display_winner(self.TABLE_TOP_PAD + self.board_size[0] * 2 + 1)
                self._display_wait_key(self.TABLE_TOP_PAD + self.board_size[0] * 2 + 2)
                self.reset_preserve_players()

    def _display_clean(self):
        """
        Clear the screen.
        """
        # Clear screen
        if self._stdscr:
            self._stdscr.clear()

    def _display_board(self, from_line: int = 0):
        """
        Display current board game.

        :param from_line: screen line where to start displaying the board.
        """
        table = self.board.as_table()
        size = self.board.size
        self._display_text((" " * 3).join(str(i) for i in range(1, size[1] + 1)), from_line, self.TABLE_LEFT_PAD + 2)
        for row_num, row in enumerate(table):
            self._display_text(chr(ord('a') + row_num) + " " + " | ".join(col or ' ' for col in row),
                               from_line + row_num * 2 + 1, self.TABLE_LEFT_PAD, )
            if row_num < size[0] - 1:
                self._display_text("--+---+--", from_line + row_num * 2 + 2, self.TABLE_LEFT_PAD + 2)

    def _display_text(self, text: str, from_line: int = 0, offset: int = 0):
        """
        Display text on screen.

        :param text: Text to display.
        :param from_line: screen line where to start displaying the text.
        :param offset: screen column where to start displaying the text.
        """
        if not self._stdscr:
            return
        try:
            self._stdscr.addstr(from_line, offset, text)
        except curses.error:
            print(self.TEXT_SMALL_DISPLAY)
            sys.exit(1)

    def _display_user_turn(self, from_line: int = 0):
        """
        Display current user turn and ask for user input if necessary.

        :param from_line: screen line where to start displaying the text.
        """
        if not self._stdscr:
            return
        self._display_text(self.TEXT_USER_TURN.format(self.current_player.name), from_line)
        if self.current_player.is_human:
            self._display_text(self.TEXT_USER_INPUT.format(self.current_player.symbol), from_line + 1)

    def _display_winner(self, from_line: int = 0):
        """
        Display winner message.

        :param from_line: screen line where to start displaying the text.
        """
        winner = self.get_winner()
        if winner:
            self._display_text(self.TEXT_WINNER.format(self.get_winner().name), from_line)

    def _display_wait_key(self, from_line: int = 0):
        """
        Display wait key message.

        :param from_line: screen line where to start displaying the text.
        """
        self._display_text(self.TEXT_WAIT_KEY, from_line, )
        return self._stdscr.getkey()

    def _display_error(self, text: str, from_line: int = 0):
        """
        Display error message to user.

        :param from_line: screen line where to start displaying the text.
        """
        self._display_clean()
        self._display_text(text, from_line)


if __name__ == '__main__':
    # Init game
    game = CliGame()
    for i in range(2):
        game.add_player()

    # Start game
    game.start()
