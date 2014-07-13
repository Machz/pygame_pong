import pygame as pg
import pong_game
import results_screen

# main window constants
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
WINDOW_TITLE = "Pong"

if __name__ == "__main__":
	pg.init()

	screen = pg.display.set_mode(SCREEN_SIZE)
	pg.display.set_caption(WINDOW_TITLE)

	while True:
		current_game = pong_game.PongGame()
		current_game.execute_game()
		print "Winner is Player {}".format(current_game.winner)
		current_results = results_screen.ResultsScreen(current_game.winner)
		current_results.display_results()
