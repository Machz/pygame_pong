import pygame, math, random
from player_bar import *

class AIBar(PlayerBar):
	START_CHECK_POS_SCREEN = .75
	ADD_TO_CHECK = .20
	GOAL_POS_CHANGE_RADIUS = 50

	def __init__(self, player_num, game_ball):
		PlayerBar.__init__(self, player_num)
		self.game_ball = game_ball
		self.last_angle_seen = None
		self.goal_pos = self.screen.get_width() / 2
		self.set_next_goal_check()
	def set_next_goal_check(self):
		self.check_goal_pos_x = AIBar.START_CHECK_POS_SCREEN * self.screen.get_width() - random.random() * (AIBar.ADD_TO_CHECK * self.screen.get_width())
	def update_pos(self):
		# update goal_pos if past check goal
		if self.game_ball.ball_angle > math.pi / 2 and self.game_ball.ball_angle < 3 * math.pi / 2 and self.last_angle_seen is not self.game_ball.ball_angle and self.game_ball.rect.left < self.check_goal_pos_x:
			self.last_angle_seen = self.game_ball.ball_angle
			x_component = math.cos(self.game_ball.ball_angle) * self.game_ball.ball_speed
			y_component = math.sin(self.game_ball.ball_angle) * self.game_ball.ball_speed
			slope = y_component / x_component
			final_y = slope * (self.game_ball.rect.left - self.rect.right) + self.game_ball.rect.centery
			self.goal_pos = final_y + random.randint(-AIBar.GOAL_POS_CHANGE_RADIUS, AIBar.GOAL_POS_CHANGE_RADIUS)
			self.set_next_goal_check()

		# move bar towards goal pos
		if not self.goal_pos - 5 < self.rect.centery < self.goal_pos + 5:
			if self.goal_pos > self.rect.centery:
				self._movement = MOVING_DOWN
			else:
				self._movement = MOVING_UP
		else:
			self._movement = NO_MOVEMENT

		PlayerBar.update_pos(self)
