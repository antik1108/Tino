"""Game engine coordinating state, entities, difficulty, and scoring."""

from tino.config import Config
from tino.engine.collision import check_collision
from tino.engine.difficulty import calculate_spawn_interval, calculate_speed
from tino.engine.entities import Obstacle, Player
from tino.engine.state import Action, GameState, is_valid_transition
from tino.storage.highscore import HighScoreStore, JSONHighScoreStore


class Game:
    """Core Game engine orchestrating the state machine and game loop ticks."""

    def __init__(
        self,
        config: Config | None = None,
        high_score_store: HighScoreStore | None = None,
        world_width: float = 80.0,
    ) -> None:
        self.config = config or Config.load()
        self.high_score_store = high_score_store or JSONHighScoreStore()
        self.world_width = world_width

        self.state = GameState.MENU
        self.high_score = self.high_score_store.load()
        self.is_new_high_score = False
        self.should_quit = False

        self.player = Player()
        self.obstacles: list[Obstacle] = []
        self.score = 0
        self.elapsed_time = 0.0
        self.current_speed = self.config.initial_speed
        self.spawn_timer = 0.0
        self.next_spawn_in = 1.5

    def transition_to(self, new_state: GameState) -> bool:
        """Safely transition to a new game state if permitted."""
        if is_valid_transition(self.state, new_state):
            self.state = new_state
            return True
        return False

    def start_game(self) -> None:
        """Start or restart a game session."""
        self.reset_run()
        self.state = GameState.PLAYING

    def reset_run(self) -> None:
        """Reset player, obstacles, score, and timings for a fresh run."""
        self.player = Player()
        self.obstacles = []
        self.score = 0
        self.elapsed_time = 0.0
        self.current_speed = self.config.initial_speed
        self.is_new_high_score = False
        self.spawn_timer = 0.0
        self.next_spawn_in = calculate_spawn_interval(
            self.current_speed,
            self.config.initial_speed,
            self.config.base_spawn_min_interval,
            self.config.base_spawn_max_interval,
        )

    def handle_action(self, action: Action) -> None:
        """Process an abstract UI action against current game state."""
        if action == Action.QUIT:
            self.should_quit = True
            return

        if self.state == GameState.MENU:
            if action in (Action.START, Action.JUMP):
                self.start_game()

        elif self.state == GameState.PLAYING:
            if action == Action.JUMP:
                self.player.jump()

        elif self.state == GameState.GAME_OVER:
            if action in (Action.RESTART, Action.START, Action.JUMP):
                self.start_game()

    def tick(self, dt: float) -> None:
        """Advance game state by dt seconds."""
        if self.state != GameState.PLAYING:
            return

        self.elapsed_time += dt
        self.score = int(self.elapsed_time * 10)  # 10 score points per second survived

        # Update difficulty & speed
        self.current_speed = calculate_speed(
            self.elapsed_time,
            initial_speed=self.config.initial_speed,
            max_speed=self.config.max_speed,
            acceleration=self.config.speed_acceleration,
        )

        # Update player physics
        self.player.update(dt)

        # Update and cull obstacles
        for obstacle in self.obstacles:
            obstacle.update(dt, self.current_speed)
        self.obstacles = [obs for obs in self.obstacles if not obs.is_offscreen]

        # Obstacle spawning
        self.spawn_timer += dt
        if self.spawn_timer >= self.next_spawn_in:
            self.spawn_timer = 0.0
            self.next_spawn_in = calculate_spawn_interval(
                self.current_speed,
                self.config.initial_speed,
                self.config.base_spawn_min_interval,
                self.config.base_spawn_max_interval,
            )
            # Spawn obstacle at the right edge
            self.obstacles.append(
                Obstacle(
                    x=self.world_width,
                    y=0.0,
                    width=3.0,
                    height=3.0,
                    obstacle_type="cactus",
                )
            )

        # Collision detection
        player_box = self.player.bounds
        for obstacle in self.obstacles:
            if check_collision(player_box, obstacle.bounds):
                self._trigger_game_over()
                break

    def _trigger_game_over(self) -> None:
        """Handle run termination on collision."""
        self.state = GameState.GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score
            self.is_new_high_score = True
            self.high_score_store.save(self.score)
