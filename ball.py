import pygame

class Ball:
	"""Pong's ball."""
	BALL_RADIUS = 8
	BALL_COLOR = pygame.Color("#000000")

	def __init__(self, screen):
		self.screen = screen
		self.x = screen.get_width() / 2
		self.y = screen.get_height() / 2
	def update(self):
		pygame.draw.circle(self.screen, Ball.BALL_COLOR, (self.x, self.y), Ball.BALL_RADIUS)
