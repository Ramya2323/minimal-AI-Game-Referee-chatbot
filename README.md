# Rock–Paper–Scissors–Plus AI Referee

## Overview
This project is a simple AI referee that runs a short game of Rock–Paper–Scissors–Plus
between a user and the bot. The referee is responsible for explaining the rules,
validating moves, keeping track of scores and rounds, and ending the game automatically
after three rounds.

The focus of this assignment is not on UI or polish, but on correct logic, clean state
management, and clear use of Google ADK concepts.

---

## How the Game Works
- The game is played for a maximum of three rounds
- At the start, the referee explains the rules in a short and clear format
- In each round, the user is asked to enter a move
- The referee validates the move, applies the game rules, and announces the result
- Scores and round number are updated after every round
- After three rounds, the game ends and the final winner is declared

Invalid inputs do not crash the game and simply consume the round, as specified.

---

## State Model
The game state is stored in a Python `dataclass` called `GameState`.  
It persists across turns and contains:
- Current round number
- User and bot scores
- Bomb usage flags for both players
- A history of all rounds played

The state is maintained explicitly in code and does not rely on prompt memory, ensuring
that game behavior is deterministic and easy to reason about.

---

## Agent and Tool Design
A single agent (`GameRefereeAgent`) controls the overall game flow and user interaction.

To keep responsibilities clear, explicit Google ADK tools are used:

- **validate_move**  
  Handles intent understanding and checks whether the user’s input is valid, including
  enforcing the “bomb can only be used once” rule.

- **resolve_round**  
  Contains the core game logic and decides the winner of each round based on the moves played.

- **update_game_state**  
  Updates the persistent game state by modifying scores, bomb usage, round count, and history.

This separation keeps input handling, game logic, and state mutation cleanly isolated.

---

## Tradeoffs
- The game runs in a simple CLI instead of a graphical interface to keep the solution minimal
- The bot uses a basic random strategy for choosing moves
- Responses are printed directly rather than returned as structured JSON

---

## What I Would Improve With More Time
- Add a smarter bot strategy instead of random moves
- Provide structured outputs for easier frontend integration
- Improve conversational responses to feel more natural
- Split responsibilities further using multiple agents if needed

---

## Note
This project uses Google ADK and is intended to run in an environment where ADK is available.
A lightweight mock was used locally only for development and testing.

