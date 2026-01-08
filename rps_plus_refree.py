import random
from dataclasses import dataclass, field
from adk.api import AdkApp, Tool
from adk.schema import Parameter


VALID_MOVES = ["rock", "paper", "scissors", "bomb"]
MAX_ROUNDS = 3

RULES = """Rules:
• Best of 3 rounds
• Moves: rock, paper, scissors, bomb (once)
• Bomb beats all, bomb vs bomb = draw
• Invalid input wastes the round
"""


@dataclass
class GameState:
    round: int = 1
    user_score: int = 0
    bot_score: int = 0
    user_bomb_used: bool = False
    bot_bomb_used: bool = False
    history: list = field(default_factory=list)


def validate_move(move: str, bomb_used: bool) -> dict:
    """Validate user move and bomb usage."""
    move = move.lower().strip()

    if move not in VALID_MOVES:
        return {"valid": False, "reason": "Invalid move"}

    if move == "bomb" and bomb_used:
        return {"valid": False, "reason": "Bomb already used"}

    return {"valid": True, "move": move}


validate_move_tool = Tool(
    name="validate_move",
    description="Validate user move and bomb usage",
    func=validate_move,
    parameters=[
        Parameter(name="move", type=str),
        Parameter(name="bomb_used", type=bool),
    ],
)


def resolve_round(user_move: str, bot_move: str) -> str:
    """Determine winner of the round."""
    if user_move == bot_move:
        return "draw"

    if user_move == "bomb":
        return "user"
    if bot_move == "bomb":
        return "bot"

    beats = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock",
    }

    return "user" if beats[user_move] == bot_move else "bot"


resolve_round_tool = Tool(
    name="resolve_round",
    description="Resolve round outcome",
    func=resolve_round,
    parameters=[
        Parameter(name="user_move", type=str),
        Parameter(name="bot_move", type=str),
    ],
)


def update_game_state(
    state: GameState,
    user_move: str,
    bot_move: str,
    winner: str,
) -> GameState:
    """Update scores, bomb usage, and round count."""
    if winner == "user":
        state.user_score += 1
    elif winner == "bot":
        state.bot_score += 1

    if user_move == "bomb":
        state.user_bomb_used = True
    if bot_move == "bomb":
        state.bot_bomb_used = True

    state.history.append({
        "round": state.round,
        "user_move": user_move,
        "bot_move": bot_move,
        "winner": winner,
    })

    state.round += 1
    return state


update_game_state_tool = Tool(
    name="update_game_state",
    description="Update game state",
    func=update_game_state,
    parameters=[
        Parameter(name="state", type=GameState),
        Parameter(name="user_move", type=str),
        Parameter(name="bot_move", type=str),
        Parameter(name="winner", type=str),
    ],
)


class GameRefereeAgent:
    def __init__(self):
        self.state = GameState()

    def bot_move(self):
        moves = ["rock", "paper", "scissors"]
        if not self.state.bot_bomb_used:
            moves.append("bomb")
        return random.choice(moves)

    def play_round(self, user_input: str):
        validation = validate_move_tool.func(
            user_input, self.state.user_bomb_used
        )

        if not validation["valid"]:
            print(f"Invalid input ({validation['reason']}). Round wasted.")
            self.state.round += 1
            return

        user_move = validation["move"]
        bot_move = self.bot_move()

        winner = resolve_round_tool.func(user_move, bot_move)

        self.state = update_game_state_tool.func(
            self.state, user_move, bot_move, winner
        )

        print(f"Round {self.state.round - 1}")
        print(f"You played: {user_move}")
        print(f"Bot played: {bot_move}")
        print(f"Winner: {winner.upper()}")

    def run(self):
        print(RULES)

        while self.state.round <= MAX_ROUNDS:
            user_input = input("Your move: ")
            self.play_round(user_input)

        print("\n--- Game Over ---")
        print(f"Final Score → You: {self.state.user_score} | Bot: {self.state.bot_score}")

        if self.state.user_score > self.state.bot_score:
            print("User wins!")
        elif self.state.bot_score > self.state.user_score:
            print("Bot wins!")
        else:
            print("Draw!")


if __name__ == "__main__":
    app = AdkApp(
        agent=GameRefereeAgent(),
        description="Rock–Paper–Scissors–Plus AI Referee"
    )
    app.run()
