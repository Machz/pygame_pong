import pygame as pg
import sys
import start_menu
import pong_game
import results_screen

# main window constants
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
WINDOW_TITLE = "Pong"

def main():
	pg.init()

	screen = pg.display.set_mode(SCREEN_SIZE)
	pg.display.set_caption(WINDOW_TITLE)

	while True:
		current_menu = start_menu.StartMenu()
		current_menu.execute()

		if current_menu.chosen_option == start_menu.ONE_PLAYER: # 1 player game
			current_game = pong_game.PongGame(1)
			current_game.execute_game()
			print "Winner is Player {}".format(current_game.winner)
			current_results = results_screen.ResultsScreen(current_game.winner)
			current_results.display_results()
		elif current_menu.chosen_option == start_menu.QUIT: # exit program
			sys.exit()

if __name__ == "__main__":
	main()
