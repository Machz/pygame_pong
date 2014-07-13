import pygame as pg
import pong_game

# main window constants
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
WINDOW_TITLE = "Pong"

if __name__ == "__main__":
	pg.init()

	screen = pg.display.set_mode(SCREEN_SIZE)
	pg.display.set_caption(WINDOW_TITLE)

	pong_game = pong_game.PongGame()
	pong_game.execute_game()
