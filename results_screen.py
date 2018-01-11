import pygame
import sys

DISPLAY_TIME = 5
RESULTS_FONT_SIZE = 75
RESULTS_FONT_COLOR = pygame.Color("#000000") # black
RESULTS_BG_COLOR = pygame.Color("#CCCCCC") # grey

class ResultsScreen:
	"""Screen to display the results of a pong game."""
	def __init__(self, player):
                # the results screen surface
		self.screen = pygame.display.get_surface()
                # the winning player
		self.player = player
		# timer for how long the results should display
		self.clock = pygame.time.Clock()
                # the font for the results
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
			# this makes the program not stall during the results screen
			for event in pygame.event.get():
				self.handle_event(event)
			time_elapsed = self.clock.tick()
			display_time -= time_elapsed

	def handle_event(self, event):
		if event.type == pygame.QUIT:
			sys.exit()
