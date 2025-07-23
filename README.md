# L-Game with AI Opponent

A Python implementation of the **L-Game**, a two-player abstract strategy board game. Players take turns moving L-shaped pieces on a 4×4 grid, strategically placing or moving neutral pieces to block their opponent. This version includes options for human vs. human, human vs. AI, and AI vs. AI gameplay with AI powered by a Minimax algorithm and alpha-beta pruning.

## Features

* 🧠 **AI Opponent** using Minimax with alpha-beta pruning
* 🧩 **Customizable Starting State**
* 👥 **Multiple Modes**: Human vs Human, Human vs AI, AI vs AI
* 🔄 **Neutral Piece Mechanics** to increase strategy depth
* 🎯 **Heuristic Evaluation** based on move availability

## How to Play

### Objective

Force your opponent into a position where they have no legal moves left.

### Game Elements

* **L1 / L2**: Two L-shaped player pieces occupying 4 grid cells
* **N**: Neutral pieces occupying 1 grid cell each
* **Grid**: 4×4 board

### Controls

On your turn, input the move using the format:

```
[y x orientation [oldNeutralY oldNeutralX newNeutralY newNeutralX]]
```

* `orientation`: n (north), s (south), e (east), w (west)
* Coordinate input is 1-indexed

Examples:

```
2 1 e              # Move only
2 1 e 2 2 3 3      # Move + neutral piece relocation
```

### Menu Flow

1. Start Game or Edit Starting State
2. Choose Mode
3. Choose First Player
4. (Optional) Enter AI search depth

## Installation

Make sure you have Python 3.x installed.
Clone the repo or copy `L-game.py` locally.

```bash
python3 L-game.py
```

## Code Structure

* `LGame`: Main game logic
* `startGame()`: Game loop handler
* `genLegalMoves()`: Generates valid L-shaped piece moves
* `chooseAiMoveMinimax()`: Uses Minimax to select best AI move
* `heuristicEvaluation()`: Evaluates board state
* `moveNeutralPiece()`: Handles logic for neutral piece manipulation

## AI Logic

* The AI searches possible moves up to a configurable depth
* Evaluates board state based on the difference in available moves
* Attempts to minimize opponent’s options by manipulating neutral pieces

## Known Limitations

* No GUI—pure terminal interaction
* Assumes valid input format
* AI might be slow on very high depth settings (≥10)

## Credits

Inspired by the original L-Game created by Edward de Bono.
AI strategy inspired by common Minimax approaches in turn-based games.

---
