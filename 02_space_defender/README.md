# Project 2: Space Defender

A real playable space shooter game built with Pygame! Defend Earth from waves of alien invaders.

## What It Does
- Control a spaceship with arrow keys or WASD
- Shoot lasers at incoming alien waves
- Dodge enemy fire and collect power-ups
- Progress through increasingly difficult waves
- Track your high score

## How to Run
```bash
cd 02_space_defender
python main.py
```

## Controls
| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Move ship |
| Space | Shoot |
| P | Pause |
| ESC | Quit |

## Python Concepts You'll Learn
- Classes and objects (Player, Enemy, Bullet, Game)
- Inheritance (different enemy types)
- Game loops and frame rate control
- Collision detection (rectangle-based)
- Coordinate systems (x, y positioning)
- Event handling (keyboard input)
- State management (menus, gameplay, game over)
- Lists and object lifecycle (spawning/destroying)

## Files
| File | What It Does |
|------|-------------|
| `main.py` | Entry point -- launches the game |
| `game.py` | Core game loop, state management, rendering |
| `sprites.py` | All game objects: Player, Enemy, Bullet, PowerUp, Star |
| `constants.py` | Game settings: colors, speeds, sizes, difficulty |

## Tech Stack
- Python
- Pygame (game engine)
