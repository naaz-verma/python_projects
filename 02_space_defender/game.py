import pygame
import random
from constants import *
from sprites import Player, Enemy, Bullet, PowerUp, Star, Explosion


class Game:
    """Main game class -- handles loop, states, rendering."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        # Game state: "menu", "playing", "paused", "game_over"
        self.state = "menu"
        self.high_score = 0
        self.stars = [Star() for _ in range(NUM_STARS)]
        self._reset_game()

    def _reset_game(self):
        """Reset all game objects for a new game."""
        self.player = Player()
        self.player_bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.powerups = []
        self.explosions = []
        self.score = 0
        self.wave = 0
        self.wave_active = False
        self.wave_timer = 0
        self.enemies_to_spawn = 0
        self.spawn_timer = 0
        self.powerup_message = ""
        self.powerup_msg_end = 0

    def run(self):
        """Main game loop."""
        running = True
        while running:
            dt = self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self._handle_event(event)

            self._update(dt)
            self._draw()
            pygame.display.flip()

        pygame.quit()

    def _handle_event(self, event):
        """Handle keyboard events based on game state."""
        if event.type != pygame.KEYDOWN:
            return

        if self.state == "menu":
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._reset_game()
                self.state = "playing"
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        elif self.state == "playing":
            if event.key == pygame.K_p:
                self.state = "paused"
            elif event.key == pygame.K_ESCAPE:
                self.state = "menu"

        elif self.state == "paused":
            if event.key == pygame.K_p or event.key == pygame.K_RETURN:
                self.state = "playing"
            elif event.key == pygame.K_ESCAPE:
                self.state = "menu"

        elif self.state == "game_over":
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._reset_game()
                self.state = "playing"
            elif event.key == pygame.K_ESCAPE:
                self.state = "menu"

    def _update(self, dt):
        """Update game logic."""
        # Stars always move
        for star in self.stars:
            star.update()

        if self.state != "playing":
            return

        keys = pygame.key.get_pressed()

        # Player
        self.player.update(keys)
        if keys[pygame.K_SPACE]:
            bullets = self.player.shoot()
            if bullets:
                self.player_bullets.extend(bullets)

        # Player bullets
        for bullet in self.player_bullets[:]:
            bullet.update()
            if bullet.is_offscreen():
                self.player_bullets.remove(bullet)

        # Enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.is_offscreen():
                self.enemy_bullets.remove(bullet)

        # Enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.is_offscreen():
                self.enemies.remove(enemy)
                continue
            # Enemy shooting
            bullet = enemy.try_shoot()
            if bullet:
                self.enemy_bullets.append(bullet)

        # Power-ups
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.is_offscreen():
                self.powerups.remove(powerup)

        # Explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if not explosion.alive:
                self.explosions.remove(explosion)

        # --- Collisions ---
        self._check_collisions()

        # --- Wave management ---
        self._manage_waves()

    def _check_collisions(self):
        """Handle all collision detection."""
        # Player bullets hitting enemies
        for bullet in self.player_bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    if enemy.take_hit():
                        self.enemies.remove(enemy)
                        self.score += POINTS_PER_ENEMY
                        self.explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                        # Power-up drop
                        if random.random() < POWERUP_DROP_CHANCE:
                            self.powerups.append(PowerUp(enemy.x, enemy.y))
                    break

        # Enemy bullets hitting player
        for bullet in self.enemy_bullets[:]:
            if bullet.rect.colliderect(self.player.rect) and not self.player.invincible:
                self.enemy_bullets.remove(bullet)
                if self.player.take_damage():
                    self._game_over()
                    return

        # Enemies colliding with player
        for enemy in self.enemies[:]:
            if enemy.rect.colliderect(self.player.rect) and not self.player.invincible:
                self.enemies.remove(enemy)
                self.explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                if self.player.take_damage():
                    self._game_over()
                    return

        # Player collecting power-ups
        for powerup in self.powerups[:]:
            if powerup.rect.colliderect(self.player.rect):
                powerup.apply(self.player)
                self.powerups.remove(powerup)
                # Show message
                messages = {
                    "rapid_fire": "RAPID FIRE!",
                    "shield": "SHIELD ACTIVE!",
                    "extra_life": "+1 LIFE!",
                }
                self.powerup_message = messages.get(powerup.type, "POWER UP!")
                self.powerup_msg_end = pygame.time.get_ticks() + 1500

    def _manage_waves(self):
        """Spawn enemy waves."""
        now = pygame.time.get_ticks()

        if not self.wave_active and len(self.enemies) == 0:
            if self.wave_timer == 0:
                self.wave_timer = now + WAVE_DELAY
            elif now >= self.wave_timer:
                # Start new wave
                self.wave += 1
                self.wave_active = True
                self.enemies_to_spawn = WAVE_BASE_ENEMIES + (self.wave - 1) * WAVE_ENEMY_INCREMENT
                self.spawn_timer = 0
                self.wave_timer = 0
                self.score += POINTS_PER_WAVE_BONUS

        if self.wave_active:
            if self.enemies_to_spawn > 0 and now - self.spawn_timer > 400:
                self.spawn_timer = now
                speed = ENEMY_BASE_SPEED + (self.wave - 1) * WAVE_SPEED_INCREMENT
                x = random.randint(20, SCREEN_WIDTH - ENEMY_WIDTH - 20)

                # Determine enemy type based on wave
                if self.wave >= 5 and random.random() < 0.2:
                    enemy_type = 2  # tough
                elif self.wave >= 3 and random.random() < 0.3:
                    enemy_type = 1  # zigzag
                else:
                    enemy_type = 0  # basic

                self.enemies.append(Enemy(x, -ENEMY_HEIGHT, speed, enemy_type))
                self.enemies_to_spawn -= 1

            if self.enemies_to_spawn <= 0:
                self.wave_active = False

    def _game_over(self):
        """Handle game over."""
        self.state = "game_over"
        if self.score > self.high_score:
            self.high_score = self.score

    def _draw(self):
        """Render everything to screen."""
        self.screen.fill(BLACK)

        # Stars (always drawn)
        for star in self.stars:
            star.draw(self.screen)

        if self.state == "menu":
            self._draw_menu()
        elif self.state == "playing":
            self._draw_gameplay()
        elif self.state == "paused":
            self._draw_gameplay()
            self._draw_pause_overlay()
        elif self.state == "game_over":
            self._draw_gameplay()
            self._draw_game_over()

    def _draw_menu(self):
        """Draw the main menu."""
        # Title
        title = self.font_large.render("SPACE DEFENDER", True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title, title_rect)

        # Subtitle
        subtitle = self.font_small.render("A WorldWithWeb Game", True, LIGHT_GRAY)
        sub_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 40))
        self.screen.blit(subtitle, sub_rect)

        # Instructions
        start_text = self.font_medium.render("Press ENTER or SPACE to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(start_text, start_rect)

        controls = [
            "Arrow Keys / WASD - Move",
            "SPACE - Shoot",
            "P - Pause",
            "ESC - Quit",
        ]
        for i, line in enumerate(controls):
            text = self.font_small.render(line, True, LIGHT_GRAY)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90 + i * 28))
            self.screen.blit(text, rect)

        if self.high_score > 0:
            hs_text = self.font_medium.render(f"High Score: {self.high_score}", True, YELLOW)
            hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
            self.screen.blit(hs_text, hs_rect)

    def _draw_gameplay(self):
        """Draw all game objects."""
        # Enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Bullets
        for bullet in self.player_bullets:
            bullet.draw(self.screen)
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)

        # Power-ups
        for powerup in self.powerups:
            powerup.draw(self.screen)

        # Explosions
        for explosion in self.explosions:
            explosion.draw(self.screen)

        # Player
        self.player.draw(self.screen)

        # HUD
        self._draw_hud()

    def _draw_hud(self):
        """Draw heads-up display: score, lives, wave."""
        # Score
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Wave
        wave_text = self.font_small.render(f"Wave: {self.wave}", True, WHITE)
        self.screen.blit(wave_text, (10, 35))

        # Lives
        lives_text = self.font_small.render(f"Lives: {'* ' * self.player.lives}", True, RED)
        self.screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))

        # Active power-ups
        y_offset = 35
        if self.player.rapid_fire:
            rf_text = self.font_small.render("RAPID FIRE", True, YELLOW)
            self.screen.blit(rf_text, (SCREEN_WIDTH - 150, y_offset))
            y_offset += 22
        if self.player.shield:
            sh_text = self.font_small.render("SHIELD", True, CYAN)
            self.screen.blit(sh_text, (SCREEN_WIDTH - 150, y_offset))

        # Power-up pickup message
        now = pygame.time.get_ticks()
        if self.powerup_message and now < self.powerup_msg_end:
            msg = self.font_medium.render(self.powerup_message, True, YELLOW)
            msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
            self.screen.blit(msg, msg_rect)

        # Wave announcement
        if self.wave_active and self.enemies_to_spawn > 0:
            wave_msg = self.font_medium.render(f"WAVE {self.wave}", True, ORANGE)
            wave_rect = wave_msg.get_rect(center=(SCREEN_WIDTH // 2, 60))
            self.screen.blit(wave_msg, wave_rect)

    def _draw_pause_overlay(self):
        """Draw pause screen overlay."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font_large.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)

        resume_text = self.font_small.render("Press P or ENTER to resume | ESC for menu", True, LIGHT_GRAY)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(resume_text, resume_rect)

    def _draw_game_over(self):
        """Draw game over screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        go_text = self.font_large.render("GAME OVER", True, RED)
        go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(go_text, go_rect)

        score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
        self.screen.blit(score_text, score_rect)

        wave_text = self.font_medium.render(f"Waves Survived: {self.wave}", True, WHITE)
        wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(wave_text, wave_rect)

        if self.score >= self.high_score and self.score > 0:
            hs_text = self.font_medium.render("NEW HIGH SCORE!", True, YELLOW)
            hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            self.screen.blit(hs_text, hs_rect)

        restart_text = self.font_small.render("Press ENTER to play again | ESC for menu", True, LIGHT_GRAY)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        self.screen.blit(restart_text, restart_rect)
