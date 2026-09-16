"""Game states and transition rules."""

from enum import Enum, auto


class GameState(Enum):
    """The discrete operational states of the game."""

    MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()


class Action(Enum):
    """Abstract actions dispatched by UI input to the engine."""

    NONE = auto()
    START = auto()
    JUMP = auto()
    RESTART = auto()
    QUIT = auto()


def is_valid_transition(current: GameState, target: GameState) -> bool:
    """Validate whether a state transition is legal."""
    valid_transitions = {
        GameState.MENU: {GameState.PLAYING},
        GameState.PLAYING: {GameState.GAME_OVER},
        GameState.GAME_OVER: {GameState.PLAYING, GameState.MENU},
    }
    return target in valid_transitions.get(current, set())
