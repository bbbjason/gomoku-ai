# Gomoku Console Game (Expandable Board)

This is a terminal-based Gomoku (Five-in-a-Row) game implemented in Python. The game features a dynamically expandable board that automatically grows when players approach the edges, supports manual expansion via command, and checks for win conditions based on user-defined alignment counts (default is five).

## Features

- Adjustable board size with automatic expansion when players move near the edges
- Manual expansion using the `larger` command
- Automatic re-centering of the board to maintain a minimum border margin
- Win condition detection for consecutive stones (default: 5 in a row)
- Simple text-based interface using coordinate input (e.g., `C3`, `D4`)

## Getting Started

### Requirements

- Python 3.6 or higher

### Running the Game

1. Save the game file as `gomoku.py`
2. Open a terminal and run:

```bash
python gomoku.py