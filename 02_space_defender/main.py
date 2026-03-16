"""
Space Defender - A WorldWithWeb Game
=====================================
Defend Earth from waves of alien invaders!

Controls:
    Arrow Keys / WASD  - Move your ship
    Space              - Shoot
    P                  - Pause
    ESC                - Quit / Menu

Run:
    python main.py
"""

from game import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
