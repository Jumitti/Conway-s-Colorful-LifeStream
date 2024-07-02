### Welcome to this little Turing machine laboratory [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://turing-machine.streamlit.app/)

## Game of Life

The Game of Life is a cellular automaton devised by the British mathematician John Horton Conway. It is a
zero-player game, meaning its evolution is determined by its initial state, requiring no further input. In this
Streamlit application, you can simulate the Game of Life with up to 3 colors. You can also adjust the rules
governing the birth and survival of cells.

Rules of Game of Life:
- **Birth**: A dead cell with exactly three live neighbors becomes alive.
- **Survival**: A live cell with two or three live neighbors survives.
- **Death**: In all other cases, a cell dies or remains dead.

## Langton's Ant

Langton's Ant is a two-dimensional universal Turing machine with very simple rules but complex emergent behavior.
In this Streamlit application, you can simulate Langton's Ant with up to 8 ants. The only modification from the
original rules is that if two ants collide on the same cell, they repel each other and move in different directions.

Rules of Langton's Ant:
- Each ant follows simple rules based on the color of the cell it's on:
  - **White**: Turn right 90 degrees.
  - **Other colors**: Turn left 90 degrees
- The grid is infinite, and ants can move in any direction.
