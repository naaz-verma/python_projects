import pygame
import random
import math
from constants import *


class Player:
    """The player's spaceship."""

    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.speed = PLAYER_SPEED
        self.lives = PLAYER_LIVES
        self.last_shot = 0
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        self.rapid_fire = False
        self.rapid_fire_end = 0
        self.shield = False
        self.shield_end = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.invincible = False
        self.invincible_end = 0
        self.visible = True
        self.blink_timer = 0

    def update(self, keys):
        """Move player based on key input."""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x = max(0, self.x - self.speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x = min(SCREEN_WIDTH - self.width, self.x + self.speed)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y = max(0, self.y - self.speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y = min(SCREEN_HEIGHT - self.height, self.y + self.speed)
        self.rect.x = self.x
        self.rect.y = self.y

        # Handle power-up timers
        now = pygame.time.get_ticks()
        if self.rapid_fire and now > self.rapid_fire_end:
            self.rapid_fire = False
            self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        if self.shield and now > self.shield_end:
            self.shield = False
        if self.invincible and now > self.invincible_end:
            self.invincible = False
            self.visible = True

        # Blink effect when invincible
        if self.invincible:
            self.blink_timer += 1
            self.visible = self.blink_timer % 10 < 5

    def shoot(self):
        """Try to fire a bullet. Returns a Bullet or None."""
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_cooldown:
            self.last_shot = now
            if self.rapid_fire:
                # Triple shot
                return [
                    Bullet(self.x + self.width // 2 - BULLET_WIDTH // 2, self.y, is_enemy=False),
                    Bullet(self.x + 4, self.y + 8, is_enemy=False),
                    Bullet(self.x + self.width - 8, self.y + 8, is_enemy=False),
                ]
            return [Bullet(self.x + self.width // 2 - BULLET_WIDTH // 2, self.y, is_enemy=False)]
        return None

    def take_damage(self):
        """Handle player getting hit. Returns True if player dies."""
        if self.invincible:
            return False
        if self.shield:
            self.shield = False
            return False
        self.lives -= 1
        self.invincible = True
        self.invincible_end = pygame.time.get_ticks() + 2000
        return self.lives <= 0

    def draw(self, screen):
        """Draw the player ship."""
        if not self.visible:
            return

        x, y = int(self.x), int(self.y)
        w, h = self.width, self.height

        # Ship body (triangle-ish shape)
        body_color = CYAN
        # Main hull
        points = [
            (x + w // 2, y),           # nose
            (x + w, y + h),            # bottom-right
            (x + w // 2, y + h - 10),  # bottom-center notch
            (x, y + h),                # bottom-left
        ]
        pygame.draw.polygon(screen, body_color, points)
        pygame.draw.polygon(screen, WHITE, points, 1)

        # Cockpit
        pygame.draw.circle(screen, BLUE, (x + w // 2, y + h // 2), 6)
        pygame.draw.circle(screen, WHITE, (x + w // 2, y + h // 2), 6, 1)

        # Engine glow
        glow_size = random.randint(4, 8)
        pygame.draw.circle(screen, ORANGE, (x + w // 2, y + h), glow_size)
        pygame.draw.circle(screen, YELLOW, (x + w // 2, y + h), glow_size // 2)

        # Shield effect
        if self.shield:
            pygame.draw.circle(screen, CYAN, (x + w // 2, y + h // 2), w // 2 + 8, 2)


class Enemy:
    """An alien enemy ship."""

    def __init__(self, x, y, speed, enemy_type=0):
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.x = x
        self.y = y
        self.speed = speed
        self.enemy_type = enemy_type  # 0=basic, 1=zigzag, 2=tough
        self.health = 1 if enemy_type < 2 else 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 1
        self.move_timer = 0
        self.zigzag_amplitude = 2

    def update(self):
        """Move the enemy downward with optional patterns."""
        self.y += self.speed
        self.move_timer += 1

        if self.enemy_type == 1:
            # Zigzag movement
            self.x += math.sin(self.move_timer * 0.05) * self.zigzag_amplitude

        # Keep in bounds horizontally
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def try_shoot(self):
        """Randomly decide to shoot. Returns Bullet or None."""
        if random.random() < ENEMY_SHOOT_CHANCE:
            return Bullet(
                self.x + self.width // 2 - ENEMY_BULLET_WIDTH // 2,
                self.y + self.height,
                is_enemy=True,
            )
        return None

    def take_hit(self):
        """Returns True if enemy is destroyed."""
        self.health -= 1
        return self.health <= 0

    def is_offscreen(self):
        return self.y > SCREEN_HEIGHT + 20

    def draw(self, screen):
        """Draw the enemy ship."""
        x, y = int(self.x), int(self.y)
        w, h = self.width, self.height

        colors = [RED, PURPLE, ORANGE]
        color = colors[self.enemy_type % len(colors)]

        # Enemy body (inverted triangle-ish)
        points = [
            (x, y),                     # top-left
            (x + w, y),                 # top-right
            (x + w // 2, y + h),       # bottom-center
        ]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, WHITE, points, 1)

        # Eye/cockpit
        pygame.draw.circle(screen, YELLOW, (x + w // 2, y + h // 3), 5)
        pygame.draw.circle(screen, BLACK, (x + w // 2, y + h // 3), 3)

        # Tough enemy indicator
        if self.enemy_type == 2 and self.health > 1:
            pygame.draw.circle(screen, WHITE, (x + w // 2, y + h // 3), 7, 2)


class Bullet:
    """A projectile fired by player or enemy."""

    def __init__(self, x, y, is_enemy=False):
        self.is_enemy = is_enemy
        if is_enemy:
            self.width = ENEMY_BULLET_WIDTH
            self.height = ENEMY_BULLET_HEIGHT
            self.speed = ENEMY_BULLET_SPEED
            self.color = RED
        else:
            self.width = BULLET_WIDTH
            self.height = BULLET_HEIGHT
            self.speed = BULLET_SPEED
            self.color = GREEN
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        """Move the bullet."""
        if self.is_enemy:
            self.y += self.speed
        else:
            self.y -= self.speed
        self.rect.y = int(self.y)

    def is_offscreen(self):
        return self.y < -20 or self.y > SCREEN_HEIGHT + 20

    def draw(self, screen):
        """Draw the bullet."""
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), self.width, self.height))
        # Glow effect
        glow_color = (150, 255, 150) if not self.is_enemy else (255, 150, 150)
        pygame.draw.rect(
            screen, glow_color,
            (int(self.x) - 1, int(self.y) - 1, self.width + 2, self.height + 2), 1
        )


class PowerUp:
    """A collectible power-up dropped by enemies."""

    TYPES = ["rapid_fire", "shield", "extra_life"]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = POWERUP_SIZE
        self.speed = POWERUP_SPEED
        self.type = random.choice(self.TYPES)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.timer = 0

    def update(self):
        """Float downward."""
        self.y += self.speed
        self.timer += 1
        self.rect.y = int(self.y)

    def is_offscreen(self):
        return self.y > SCREEN_HEIGHT + 20

    def apply(self, player):
        """Apply the power-up effect to the player."""
        now = pygame.time.get_ticks()
        if self.type == "rapid_fire":
            player.rapid_fire = True
            player.rapid_fire_end = now + POWERUP_DURATION
            player.shoot_cooldown = PLAYER_SHOOT_COOLDOWN // 3
        elif self.type == "shield":
            player.shield = True
            player.shield_end = now + SHIELD_DURATION
        elif self.type == "extra_life":
            player.lives = min(player.lives + 1, 5)

    def draw(self, screen):
        """Draw the power-up with a pulsing effect."""
        x, y = int(self.x), int(self.y)
        pulse = int(math.sin(self.timer * 0.1) * 3)
        size = self.size + pulse

        if self.type == "rapid_fire":
            color = YELLOW
            label = "R"
        elif self.type == "shield":
            color = CYAN
            label = "S"
        else:
            color = GREEN
            label = "+"

        pygame.draw.rect(screen, color, (x - pulse // 2, y - pulse // 2, size, size), border_radius=6)
        pygame.draw.rect(screen, WHITE, (x - pulse // 2, y - pulse // 2, size, size), 1, border_radius=6)

        font = pygame.font.Font(None, 20)
        text = font.render(label, True, BLACK)
        text_rect = text.get_rect(center=(x + self.size // 2, y + self.size // 2))
        screen.blit(text, text_rect)


class Star:
    """A background star for parallax scrolling effect."""

    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(STAR_MIN_SPEED, STAR_MAX_SPEED)
        self.brightness = random.randint(80, 255)
        self.size = 1 if self.speed < 2 else 2

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)


class Explosion:
    """Visual explosion effect when enemies are destroyed."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particles = []
        for _ in range(12):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 4)
            self.particles.append({
                "x": x,
                "y": y,
                "dx": math.cos(angle) * speed,
                "dy": math.sin(angle) * speed,
                "life": random.randint(10, 25),
                "color": random.choice([RED, ORANGE, YELLOW, WHITE]),
                "size": random.randint(2, 5),
            })
        self.alive = True

    def update(self):
        self.alive = False
        for p in self.particles:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            p["life"] -= 1
            p["size"] = max(0, p["size"] - 0.1)
            if p["life"] > 0:
                self.alive = True

    def draw(self, screen):
        for p in self.particles:
            if p["life"] > 0 and p["size"] > 0:
                pygame.draw.circle(
                    screen,
                    p["color"],
                    (int(p["x"]), int(p["y"])),
                    int(p["size"]),
                )
