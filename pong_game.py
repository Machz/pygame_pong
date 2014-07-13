import pygame
import player_bar, ball, score

MAX_FPS = 60
SCREEN_BACKGROUND = pygame.Color("#cccccc")
MY_PLAYER = 2 # this client's player

class PongGame:
	def __init__(self):
		# get current surface
		self.screen = pygame.display.get_surface()

		# create clock used for FPS
		self.clock = pygame.time.Clock()

		# create game objects
		self.game_ball = ball.Ball(self.screen)
		self.player_bars = [ player_bar.PlayerBar(self.screen, 1), player_bar.PlayerBar(self.screen, 2) ]
		self.game_score = score.Score(self.screen)

		# set allowed events (or disallowed.. whatever)
		pygame.event.set_allowed(None)
		pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

		# pong game runs while this is true
		self._running = True
	def handle_event(self, event):
		"""Handles PyGame events during a Pong game."""
		if event.type == pygame.KEYDOWN:
			# key pushed
			if event.__dict__['key'] == self.player_bars[MY_PLAYER-1].controls['up']:
				self.player_bars[MY_PLAYER-1].movement = player_bar.MOVING_UP
			elif event.__dict__['key'] == self.player_bars[MY_PLAYER-1].controls['down']:
				self.player_bars[MY_PLAYER-1].movement = player_bar.MOVING_DOWN
		elif event.type == pygame.KEYUP:
			# key raised
			if event.__dict__['key'] == self.player_bars[MY_PLAYER-1].controls['up'] and self.player_bars[MY_PLAYER-1].movement == player_bar.MOVING_UP:
				self.player_bars[MY_PLAYER-1].movement = player_bar.NO_MOVEMENT
			elif event.__dict__['key'] == self.player_bars[MY_PLAYER-1].controls['down'] and self.player_bars[MY_PLAYER-1].movement == player_bar.MOVING_DOWN:
				self.player_bars[MY_PLAYER-1].movement = player_bar.NO_MOVEMENT
		elif event.type == pygame.QUIT:
			sys.exit()
	def logic_loop(self):
		"""Main loop logic."""
		# limit FPS
		self.clock.tick(MAX_FPS)

		# move players' bars (if needed)
		self.player_bars[0].move()
		self.player_bars[1].move()
	def render_objects(self):
		"""Render an updated game screen."""
		# update objects displayed on screen
		self.screen.fill(SCREEN_BACKGROUND)
		self.game_ball.update()
		self.player_bars[0].update()
		self.player_bars[1].update()
		self.game_score.update()

		# render the updated Surface
		pygame.display.flip()
	def execute_game(self):
		"""Main game loop."""
		while self._running:
			for event in pygame.event.get():
				self.handle_event(event)
			self.logic_loop()
			self.render_objects()
		
