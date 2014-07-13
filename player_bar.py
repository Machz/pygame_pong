import pygame

class PlayerBar:
	"""The players' bars used to hit the pong ball back and forth."""
	BAR_VSPEED = 6 # vertical speed of bars
	BAR_HEIGHT = 100
	BAR_WIDTH = 20
	BAR_COLOR = pygame.Color("#000000")
	# self._movement value codes
	NO_MOVEMENT = 0
	MOVING_UP = 1
	MOVING_DOWN = -1
	def __init__(self, screen, player_num):
		self.screen = screen
		self.player_num = player_num
		self._movement = PlayerBar.NO_MOVEMENT
		# set bar's initial position
		if self.player_num == 1:
			self.rect = pygame.Rect(PlayerBar.BAR_WIDTH, screen.get_height() / 2 - PlayerBar.BAR_HEIGHT / 2, PlayerBar.BAR_WIDTH, PlayerBar.BAR_HEIGHT)
		elif self.player_num == 2:
			self.rect = pygame.Rect(screen.get_width() - 2*PlayerBar.BAR_WIDTH, screen.get_height() / 2 - PlayerBar.BAR_HEIGHT / 2, PlayerBar.BAR_WIDTH, PlayerBar.BAR_HEIGHT)
	# movement stuff
	def get_movement(self):
		return self._movement
	def set_movement(self, new_movement):
		"""Sets a new value for self.movement"""
		if not (-1 <= new_movement <= 1):
			raise Exception("new_movement value must be -1 <= new_movement <= 1")
		self._movement = new_movement
	movement = property(get_movement, set_movement)
	def move(self):
		"""Moves a player's bar if needed."""
		if self.movement == PlayerBar.MOVING_UP:
			self.rect.y += -PlayerBar.BAR_VSPEED
			if self.rect.top < 0:
				self.rect.top = 0
		elif self.movement == PlayerBar.MOVING_DOWN:
			self.rect.y += PlayerBar.BAR_VSPEED
			if self.rect.bottom > self.screen.get_height():
				self.rect.bottom = self.screen.get_height()
	def update(self):
		"""Re-draws the player's bar on self.screen."""
		pygame.draw.rect(self.screen, PlayerBar.BAR_COLOR, self.rect)
