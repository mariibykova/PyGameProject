from for_game.start import start_starting_window
from for_game.game import start_the_game
import pygame


def main():
    try:
        print("Starting the game...")
        game_running = start_starting_window()
        while game_running:
            start_the_game()
    except pygame.error:
        pass


if __name__ == "__main__":
    main()
