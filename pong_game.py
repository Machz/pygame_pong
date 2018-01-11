import pygame
import sys
import player_bar, ai_bar, ball, score

MAX_FPS = 60
SCREEN_BACKGROUND = pygame.Color("#cccccc")
MY_PLAYER = 2 # this client's player
PLAYER_SCORED = pygame.USEREVENT
COUNTDOWN_LENGTH = 3
COUNTDOWN_FONT_SIZE = 75
COUNTDOWN_FONT_COLOR = pygame.Color("#000000")
ONE_PLAYER_MODE = 1
SCORE_TO_WIN = 3

class PongGame:
	def __init__(self, game_type):
		# get current surface
		self.screen = pygame.display.get_surface()

		# set game type
		self.game_type = game_type

		# create clock used for FPS
		self.clock = pygame.time.Clock()

		# create game objects
		self.game_ball = ball.Ball(self.screen, player_bar.BAR_VSPEED - 2)
		if game_type == ONE_PLAYER_MODE:
			self.player_bars = [ ai_bar.AIBar(1, self.game_ball), player_bar.PlayerBar(2) ]
		self.game_score = score.Score(self.screen)

		# set allowed events (or disallowed.. whatever)
		pygame.event.set_allowed(None)
		pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, PLAYER_SCORED])

		# pong game runs while this is true
		self._player_won = False

	def do_countdown(self, length):
		"""Does a countdown before starting a round.
		
		length is in seconds."""
		self.render_objects()
		countdown_length = length * 1000
		countdown_font = pygame.font.Font(None, COUNTDOWN_FONT_SIZE)
		while countdown_length > 0:
			for event in pygame.event.get():
				self.handle_event(event)
			time_elapsed = self.clock.tick(MAX_FPS)
			countdown_length -= time_elapsed
			countdown_string = str(countdown_length / 1000 + 1)
			if countdown_string == '0': countdown_string = '1'
			countdown_surface = countdown_font.render(countdown_string, True, COUNTDOWN_FONT_COLOR)
			countdown_draw_area = pygame.Rect(self.screen.get_width() / 2 - countdown_surface.get_width() / 2,
								self.screen.get_height() / 2 - countdown_surface.get_height() / 2,
								countdown_surface.get_width(),
								countdown_surface.get_height())
			pygame.draw.rect(self.screen, SCREEN_BACKGROUND, countdown_draw_area)
			self.screen.blit(countdown_surface, (countdown_draw_area.x, countdown_draw_area.y))
			pygame.display.flip()

	def handle_event(self, event):
		"""Handles PyGame events during a Pong game."""
		global MY_PLAYER
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
		elif event.type == PLAYER_SCORED:
			if self.game_score.add_point(event.__dict__['player']) < SCORE_TO_WIN:
				self.game_ball.reset()
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

		# update ball speed
		self.game_ball.update_speed(time_elapsed)

		# see if a player has scored
		self.game_ball.check_scored()

		# update positions
		self.game_ball.update_pos()
		self.player_bars[0].update_pos()
		self.player_bars[1].update_pos()

		# check for collisions
		self.game_ball.check_collisions([self.player_bars[0].rect, self.player_bars[1].rect])

	def render_objects(self):
		"""Render an updated game screen."""
		# update objects displayed on screen
		self.screen.fill(SCREEN_BACKGROUND)

		self.game_ball.render()
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
