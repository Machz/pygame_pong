import pygame

class Score:
	SCORE_FONT_SIZE = 50
	SCORE_FONT_COLOR = pygame.Color("#000000")
	SCORE_VERT_POS = 20
	def __init__(self, screen):
		self.screen = screen
		self.scores = [ 0, 0 ]
		self.font = pygame.font.Font(None, Score.SCORE_FONT_SIZE)
	def add_point(self, player):
		"""Player scored! Now add a point."""
		self.scores[player-1] += 1
		return self.scores[player-1]
	def render(self):
		score_string = "{} | {}".format(self.scores[0], self.scores[1])
		score_surface = self.font.render(score_string, True, Score.SCORE_FONT_COLOR)
		self.screen.blit(score_surface, (self.screen.get_width() / 2 - score_surface.get_width() / 2, Score.SCORE_VERT_POS))
