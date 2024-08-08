from ui import CliGame

if __name__ == '__main__':
    # Init game
    game = CliGame()
    for i in range(2):
        game.add_player()

    # Start game
    game.start()
