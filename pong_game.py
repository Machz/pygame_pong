import pygame
import sys
import player_bar, ball, score

MAX_FPS = 60
SCREEN_BACKGROUND = pygame.Color("#cccccc")
MY_PLAYER = 1 # this client's player
PLAYER_SCORED = pygame.USEREVENT
COUNTDOWN_LENGTH = 3
COUNTDOWN_FONT_SIZE = 75
COUNTDOWN_FONT_COLOR = pygame.Color("#000000")

class PongGame:
	def __init__(self):
		# get current surface
		self.screen = pygame.display.get_surface()

		# create clock used for FPS
		self.clock = pygame.time.Clock()

		# create game objects
		self.game_ball = ball.Ball(self.screen, player_bar.BAR_VSPEED - 5)
		self.player_bars = [ player_bar.PlayerBar(self.screen, 1), player_bar.PlayerBar(self.screen, 2) ]
		self.game_score = score.Score(self.screen)

		# set allowed events (or disallowed.. whatever)
		pygame.event.set_allowed(None)
		pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, PLAYER_SCORED])

		# pong game runs while this is true
		self._player_won = False
	def do_countdown(self, length):
		"""Does a countdown before starting a round.
		
		length is in seconds."""
		countdown_length = length * 1000
		countdown_font = pygame.font.Font(None, COUNTDOWN_FONT_SIZE)
		while countdown_length > 0:
			time_elapsed = self.clock.tick(MAX_FPS)
			countdown_length -= time_elapsed
			countdown_string = str(countdown_length / 1000 + 1)
			self.countdown_surface = countdown_font.render(countdown_string, True, COUNTDOWN_FONT_COLOR)
			# self.screen.blit(countdown_surface, (self.screen.get_width() / 2 - countdown_surface.get_width() / 2, 
			self.render_objects()
		self.countdown_surface = None
							     #self.screen.get_height() / 2 + countdown_surface.get_height() / 2))
	def handle_event(self, event):
		"""Handles PyGame events during a Pong game."""
		if event.type == pygame.KEYDOWN:
			# key pushed
			if event.__dict__['key'] == self.player_bars[MY_PLAYER-1].controls['up']:
				self.player_bars[MY_PLAYER-1].movement = player_bar.MOVING_UP
			elif event.__dict__['key'] == self.player_bars[MY_PLAYER-1].controls['down']:
				self.player_bars[MY_PLAYER-1].movement = player_bar.MOVING_DOWN
			elif event.__dict__['key'] == ord('a'):
				global MY_PLAYER
				if MY_PLAYER == 2:
					MY_PLAYER = 1
				else:
					MY_PLAYER = 2
		elif event.type == pygame.KEYUP:
			# key raised
			if event.__dict__['key'] == self.player_bars[MY_PLAYER-1].controls['up'] and self.player_bars[MY_PLAYER-1].movement == player_bar.MOVING_UP:
				self.player_bars[MY_PLAYER-1].movement = player_bar.NO_MOVEMENT
			elif event.__dict__['key'] == self.player_bars[MY_PLAYER-1].controls['down'] and self.player_bars[MY_PLAYER-1].movement == player_bar.MOVING_DOWN:
				self.player_bars[MY_PLAYER-1].movement = player_bar.NO_MOVEMENT
		elif event.type == PLAYER_SCORED:
			if self.game_score.add_point(event.__dict__['player']) < 1:
				self.game_ball = ball.Ball(self.screen, player_bar.BAR_VSPEED - 5)
			else:
				self._player_won = event.__dict__['player']
		elif event.type == pygame.QUIT:
			sys.exit()
		else:
			print "Event :.:.: {} = {}".format(event.type, event.__dict__)
	def logic_loop(self):
		"""Main loop logic."""
		# limit FPS
		time_elapsed = self.clock.tick(MAX_FPS)

		# update ball stuff 
		self.game_ball.update_speed(time_elapsed)
		self.game_ball.update_pos()
		self.game_ball.check_collisions([self.player_bars[0].rect, self.player_bars[1].rect])

		# see if a player has scored
		self.game_ball.check_scored()

		# move players' bars (if needed)
		self.player_bars[0].update_pos()
		self.player_bars[1].update_pos()
	def render_objects(self):
		"""Render an updated game screen."""
		# update objects displayed on screen
		self.screen.fill(SCREEN_BACKGROUND)

		# render ball if no countdown is currently going
		if not self.countdown_surface:
			self.game_ball.render()
		else:
			self.screen.blit(self.countdown_surface,
					(self.screen.get_width() / 2 - self.countdown_surface.get_width() / 2,
					self.screen.get_height() / 2 - self.countdown_surface.get_height() / 2))

		self.player_bars[0].render()
		self.player_bars[1].render()
		self.game_score.render()

		# render the updated Surface
		pygame.display.flip()
	def execute_game(self):
		"""Main game loop."""
		self.do_countdown(COUNTDOWN_LENGTH)
		while not self._player_won:
			for event in pygame.event.get():
				self.handle_event(event)
			self.logic_loop()
			self.render_objects()
	def get_winner(self):
		return self._player_won
	winner = property(get_winner)