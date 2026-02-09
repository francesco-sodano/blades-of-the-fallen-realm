"""Game constants and configuration for Blades of the Fallen Realm."""

# --- Display ---
SCREEN_WIDTH: int = 960
SCREEN_HEIGHT: int = 540
BASE_WIDTH: int = 480
BASE_HEIGHT: int = 270
SCALE_FACTOR: int = 2
FPS: int = 60
GAME_TITLE: str = "Blades of the Fallen Realm"

# --- Physics ---
GRAVITY: float = 0.5
GROUND_FRICTION: float = 0.85
WALK_SPEED: float = 2.5
RUN_SPEED: float = 4.0
JUMP_FORCE: float = -8.0

# --- Pseudo-3D depth ---
DEPTH_BAND_MIN: int = 160  # Top of walkable depth band (Y)
DEPTH_BAND_MAX: int = 260  # Bottom of walkable depth band (Y)
DEPTH_PROXIMITY: int = 15  # Y-axis tolerance for attacks to connect

# --- Camera ---
SCROLL_SPEED: float = 2.0
PARALLAX_FAR: float = 0.3
PARALLAX_MID: float = 0.6
PARALLAX_NEAR: float = 1.0
PLAYER_LEASH: int = 400  # Max pixels a player can be off-screen edge

# --- Combat ---
COMBO_WINDOW_MS: int = 500  # Milliseconds to chain combo inputs
INVINCIBILITY_FRAMES: int = 60  # Frames of invincibility after hit/respawn
MAX_MAGIC_CHARGES: int = 9
GRAB_RANGE: int = 30  # Pixels proximity for throw/grab

# --- Spawn ---
MAX_ENEMIES_SOLO: int = 6
MAX_ENEMIES_COOP: int = 8
COOP_SPAWN_MULTIPLIER: float = 1.5
COOP_BOSS_HP_MULTIPLIER: float = 1.4

# --- Lives & Scoring ---
STARTING_LIVES: int = 3
MAX_CONTINUES: int = 3
CONTINUE_COUNTDOWN: int = 10  # Seconds
EXTRA_LIFE_THRESHOLDS: list[int] = [50_000, 100_000]

# --- Score values ---
SCORE_BOGWORT_GRUNT: int = 100
SCORE_BOGWORT_ARCHER: int = 150
SCORE_BOGWORT_WITCH: int = 200
SCORE_SNARLFANG_RIDER: int = 250
SCORE_IRONHIDE_BRUTE: int = 300
SCORE_IRONHIDE_RAVAGER: int = 350
SCORE_STONE_TROLL: int = 500
SCORE_BOSS: int = 2000
SCORE_NO_DAMAGE_WAVE: int = 500

# --- Camp scene ---
CAMP_DURATION_SECONDS: int = 15
PIXI_SPAWN_SOLO: int = 2
PIXI_SPAWN_COOP: int = 3

# --- Player controls ---
P1_CONTROLS: dict[str, int] = {}  # Populated at runtime with pygame key constants
P2_CONTROLS: dict[str, int] = {}  # Populated at runtime with pygame key constants

# --- Colors ---
COLOR_BLACK: tuple[int, int, int] = (0, 0, 0)
COLOR_WHITE: tuple[int, int, int] = (255, 255, 255)
COLOR_RED: tuple[int, int, int] = (255, 0, 0)
COLOR_GREEN: tuple[int, int, int] = (0, 255, 0)
COLOR_BLUE: tuple[int, int, int] = (0, 0, 255)
COLOR_YELLOW: tuple[int, int, int] = (255, 255, 0)
