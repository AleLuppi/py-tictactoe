from game import BaseGame, Player


class CliGame(BaseGame):
    @staticmethod
    def get_user_play(player: Player) -> str:
        return input(f"{player.name or 'User'}'s turn: ")


if __name__ == '__main__':
    # Init game
    game = CliGame()
    for i in range(2):
        game.add_player()

    # Step game
    while game.step():
        table = game.board.as_table()
        table_str = "\n--+---+--\n".join([" | ".join(col or ' ' for col in row) for row in table])
        print(table_str)
