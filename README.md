# Chess Engine (Minimax & Optimization)

A Python-based chess bot developed with a focus on **Algorithm Optimization** and **Search Efficiency**.

## Key Features & Optimization Techniques

The engine implements several industry-standard optimization techniques to improve search depth and speed:

* **Minimax Algorithm with Alpha-Beta Pruning**: Significantly reduces the number of nodes evaluated in the search tree, allowing for deeper look-ahead.
* **Transposition Table (Caching)**: Uses a Global Hash Map (FEN-based) to store and reuse previously calculated board states, preventing redundant computations.
* **Iterative Deepening**: Progressively increases search depth within a strict **Time Limit**, ensuring the bot always returns the best found move without crashing the system clock.
* **Quiescence Search**: Solves the "Horizon Effect" by continuing the search through capture sequences, ensuring stable board evaluations.
* **Move Ordering**: Prioritizes captures, promotions, and checks to maximize the efficiency of Alpha-Beta Pruning.
* **Advanced Evaluation Function**:
    * **Material Weighting**: Standard piece value analysis.
    * **Piece-Square Tables (PST)**: Encourages positional play (e.g., Knights in the center, Pawns advancing).
    * **Mobility Scoring**: Rewards positions with higher legal move availability.

## Tech Stack
- **Language**: Python 3.x
- **Core Library**: `python-chess`
- **Logic**: Strategic heuristic evaluation and recursive search optimization.

## Project Structure
- `AI.py`: Contains the core Minimax logic and evaluation heuristics.
- `get_bot_move`: The main entry point for iterative deepening search.
- `Transposition Table`: Global cache management for performance scaling.

## Author
- **Pham Anh Tu**
- **University**: Hanoi University of Science and Technology (HUST)
- **Affiliation**: EdgeAI Lab 802
- **Focus**: Optimization & Cyber Security
