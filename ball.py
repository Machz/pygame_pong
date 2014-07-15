import pygame as pg
import math, random
import pong_game
import player_bar

BALL_RADIUS = 8
BALL_COLOR = pg.Color("#000000")
SPEED_UPDATE_DELAY = 3
SPEED_INCREMENT = 2
START_ANGLES = [ (1.0/24.0)*2*math.pi, (3.0/24.0)*2*math.pi, (9.0/24.0)*2*math.pi, (11.0/24.0)*2*math.pi, (13.0/24.0)*2*math.pi, (15.0/24.0)*2*math.pi, (21.0/24.0)*2*math.pi, (23.0/24.0)*2*math.pi, ]

class Ball:
	"""Pong's ball."""

	def __init__(self, screen, ball_start_speed):
		self.screen = screen

		# rect for ball -- have to use conversions to find exact position of end of ball if needed
		self.rect = pg.Rect(screen.get_width() / 2 - BALL_RADIUS, screen.get_height() / 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

		# speed stuff for ball -- math time!
		self.ball_speed = self.ball_start_speed = ball_start_speed
		self.last_speed_update = 0

		# setting initial ball angle, making sure that it's not too vertical or horizontal
		self.ball_angle = random.choice(START_ANGLES)

		self.update_speed_vec()
	def update_speed(self, time_elapsed):
		self.last_speed_update += time_elapsed
		if self.last_speed_update >= SPEED_UPDATE_DELAY * 1000:
			self.ball_speed += SPEED_INCREMENT
			self.update_speed_vec()
			self.last_speed_update = 0
	def update_speed_vec(self):
		self.speed_vec = [ math.cos(self.ball_angle) * self.ball_speed, -math.sin(self.ball_angle) * self.ball_speed ]
	def update_pos(self):
		self.rect.move_ip(*self.speed_vec)
	def check_collisions(self, bar_rects):
		"""Checks if the ball has collided with the top/bottom walls or a player's bar."""
		if self.rect.top < 0:
			self.rect.top = 0
			self.ball_angle = 2*math.pi - self.ball_angle
			self.update_speed_vec()
		elif self.rect.bottom > self.screen.get_height():
			self.rect.bottom = self.screen.get_height()
			self.ball_angle = 2*math.pi - self.ball_angle
			self.update_speed_vec()
		for rect in bar_rects:
			height_diff = abs(self.rect.top - rect.bottom)
			max_height_diff = (BALL_RADIUS*2 + player_bar.BAR_HEIGHT)
			next_rect = self.rect.move(*self.speed_vec)
			if self.rect.right <= rect.left <= next_rect.right and next_rect.bottom >= rect.top and next_rect.top <= rect.bottom:
				# based on ball pos relative to bar
				self.ball_angle = math.pi + (1.0 * (self.rect.top - rect.centery) / (max_height_diff / 2.0))
				# just bounce
				#self.ball_angle = math.pi - self.ball_angle
				self.update_speed_vec()
				self.rect.right = rect.left
			elif self.rect.left >= rect.right >= next_rect.left and next_rect.bottom >= rect.top and next_rect.top <= rect.bottom:
				self.ball_angle = 1.0 * (rect.centery - self.rect.top) / (max_height_diff / 2.0)
				#self.ball_angle = math.pi - self.ball_angle
				self.update_speed_vec()
				self.rect.left = rect.right
	def check_scored(self):
		"""Checks if the ball has hit the left/right wall. (Meaning a player has scored.)"""
		if self.rect.left <= 0:
			event = pg.event.Event(pong_game.PLAYER_SCORED, { 'player': 2 })
			pg.event.post(event)
			return 2
		elif self.rect.right >= self.screen.get_width():
			event = pg.event.Event(pong_game.PLAYER_SCORED, { 'player': 1 })
			pg.event.post(event)
			return 1
		else:
			return False
	def reset(self):
		self.__init__(self.screen, self.ball_start_speed)
	def render(self):
		pg.draw.circle(self.screen, BALL_COLOR, self.rect.center, BALL_RADIUS)
