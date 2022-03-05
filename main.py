import pygame, os
import game_lib

def main():
    game = game_lib.Game()
    game.setup()
    quit_game = False
    while not quit_game:
        quit_game = game.swap_screen()


if __name__ == "__main__":
    main()