import pygame

DISPLAY_TIME = 5
RESULTS_FONT_SIZE = 75
RESULTS_FONT_COLOR = pygame.Color("#000000") # black
RESULTS_BG_COLOR = pygame.Color("#CCCCCC") # grey

class ResultsScreen:
	"""Screen to display the results of a pong game."""
	def __init__(self, player):
		self.screen = pygame.display.get_surface()
		self.player = player

		# timer for how long the results should display
		self.clock = pygame.time.Clock()

		self.results_font = pygame.font.Font(None, RESULTS_FONT_SIZE)

	def display_results(self):
		display_time = DISPLAY_TIME * 1000

		results_string = "Winner is Player {}!".format(self.player)
		results_surface = self.results_font.render(results_string, True, RESULTS_FONT_COLOR)

		# render results
		self.screen.fill(RESULTS_BG_COLOR)
		self.screen.blit(results_surface,
				(self.screen.get_width() / 2 - results_surface.get_width() / 2,
					self.screen.get_height() / 2 - results_surface.get_height() / 2))
		pygame.display.flip()

		while display_time > 0:
			time_elapsed = self.clock.tick()
			display_time -= time_elapsed
			
