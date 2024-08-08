# Python TicTacToe game

**An (almost) deps-free Tic-Tac-Toe game built in python**

Why "_almost_" deps-free? Because `curses` module dependency is already satisfied by standard library...
with no support for Windows. Thus, on "Windows" machine, `windows-curses` shall be installed.

## Get started

> Tested on **Python3.10**

Start playing in a minute following the steps:

1. Clone the repo:

   ```console
   git clone https://github.com/AleLuppi/py-tictactoe.git
   cd py-tictactoe
   ```

2. Install requirements **(Windows only)**:

   ```console
   pip install -r requirements.txt
   ```

3. Start the game

   ```console
   python src/main.py
   ```

## Next steps (/w hints)

Some new features are along the way.
Here's how next updates may look like:

- **Enable larger field game**

  Ever tried a 4x4 TicTacToe? Or 5x5? Or 1000x1000?

  Not sure if funny to play, but for sure funny to code!
  Larger boards are already supported up to 9x9, just need `*Game` to init appropriately.

- **Play against bot**

  Not everyone has a friend who wants to play TicTacToe :(

  But anyone can have a friendly bot to play against!
  Just implement `Player.play` logic for non-human players.

- **Multi-multiplayer**

  For coolest parties ever, play against 4-5 friends.

  Current implementation supports up to 6 players, but can be easily extended by adding new playing symbols.

- **Game config**

  What if you want to change name, or your hero symbol?

  A game config should allow it. Easy-peasy as long as `*Game` allows setting its config from UI.

- **GUI**

  Who wants terminal, when they can have GRAPHICS?

  Just create a `GuiGame` to display graphical elements! "Just"...

- **3D TicTacToe**

  This is actually not supported right now, but might be cool.
