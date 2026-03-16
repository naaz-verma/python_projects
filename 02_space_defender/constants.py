# --- Display ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Space Defender - WorldWithWeb"

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 50)
ORANGE = (255, 165, 0)
PURPLE = (180, 100, 255)
CYAN = (0, 255, 255)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (180, 180, 180)

# --- Player ---
PLAYER_SPEED = 5
PLAYER_WIDTH = 48
PLAYER_HEIGHT = 48
PLAYER_LIVES = 3
PLAYER_SHOOT_COOLDOWN = 250  # milliseconds

# --- Bullets ---
BULLET_SPEED = 7
BULLET_WIDTH = 4
BULLET_HEIGHT = 12
ENEMY_BULLET_SPEED = 4
ENEMY_BULLET_WIDTH = 4
ENEMY_BULLET_HEIGHT = 10

# --- Enemies ---
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
ENEMY_BASE_SPEED = 1.5
ENEMY_SHOOT_CHANCE = 0.005  # per frame per enemy

# --- Power-ups ---
POWERUP_SIZE = 24
POWERUP_SPEED = 2
POWERUP_DROP_CHANCE = 0.15  # chance an enemy drops a power-up on death
POWERUP_DURATION = 5000  # milliseconds
SHIELD_DURATION = 8000

# --- Waves ---
WAVE_BASE_ENEMIES = 6
WAVE_ENEMY_INCREMENT = 2  # extra enemies per wave
WAVE_SPEED_INCREMENT = 0.3  # speed increase per wave
WAVE_DELAY = 2000  # milliseconds between waves

# --- Stars (background) ---
NUM_STARS = 80
STAR_MIN_SPEED = 1
STAR_MAX_SPEED = 3

# --- Scoring ---
POINTS_PER_ENEMY = 100
POINTS_PER_WAVE_BONUS = 500
