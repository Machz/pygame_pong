import pygame

BAR_VSPEED = 10 # vertical speed of bars
BAR_HEIGHT = 100
BAR_WIDTH = 20
BAR_COLOR = pygame.Color("#000000")
# self._movement value codes
NO_MOVEMENT = 0
MOVING_UP = 1
MOVING_DOWN = -1

class PlayerBar:
	"""The players' bars used to hit the pong ball back and forth."""
	def __init__(self, player_num):
		self.screen = pygame.display.get_surface()
		self.player_num = player_num
		self._movement = NO_MOVEMENT
		if self.__class__.__name__ is "PlayerBar":
			if player_num is 2:
				self.controls = {'up': 273, 'down': 274}
		# set bar's initial position
		if self.player_num == 1:
			self.rect = pygame.Rect(BAR_WIDTH, self.screen.get_height() / 2 - BAR_HEIGHT / 2, BAR_WIDTH, BAR_HEIGHT)
		elif self.player_num == 2:
			self.rect = pygame.Rect(self.screen.get_width() - 2*BAR_WIDTH, self.screen.get_height() / 2 - BAR_HEIGHT / 2, BAR_WIDTH, BAR_HEIGHT)
	# movement stuff
	def get_movement(self):
		return self._movement
	def set_movement(self, new_movement):
		"""Sets a new value for self.movement"""
		if not (-1 <= new_movement <= 1):
			raise Exception("new_movement value must be -1 <= new_movement <= 1")
		self._movement = new_movement
	movement = property(get_movement, set_movement)
	def update_pos(self):
		"""Moves a player's bar if needed."""
		if self.movement == MOVING_UP:
			self.rect.y += -BAR_VSPEED
			if self.rect.top < 0:
				self.rect.top = 0
		elif self.movement == MOVING_DOWN:
			self.rect.y += BAR_VSPEED
			if self.rect.bottom > self.screen.get_height():
				self.rect.bottom = self.screen.get_height()
	def render(self):
		"""Re-draws the player's bar on self.screen."""
		pygame.draw.rect(self.screen, BAR_COLOR, self.rect)
