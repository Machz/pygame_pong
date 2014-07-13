import pygame
import player_bar
import ball
import score

# constants
WINDOW_TITLE = "Pong"
MAX_FPS = 60
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_BACKGROUND = pygame.Color("#cccccc")
UP_ARROW_KEY = 273
DOWN_ARROW_KEY = 274
MY_PLAYER = 2 # this client's player

# initialize pygame modules
pygame.init()

# set up the main game window
screen = pygame.display.set_mode(SCREEN_SIZE) # main Surface
pygame.display.set_caption(WINDOW_TITLE)

# create clock used for FPS
clock = pygame.time.Clock() 

# create objects used for game
game_ball = ball.Ball(screen)
player_bars = [ player_bar.PlayerBar(screen, 1), player_bar.PlayerBar(screen, 2) ]
game_score = score.Score(screen)

# set allowed events (or disallowed.. whatever)
pygame.event.set_allowed(None)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

while True:
	# handle pygame events
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			# key pushed
			if event.__dict__['key'] == UP_ARROW_KEY:
				player_bars[MY_PLAYER-1].movement = player_bar.PlayerBar.MOVING_UP
			elif event.__dict__['key'] == DOWN_ARROW_KEY:
				player_bars[MY_PLAYER-1].movement = player_bar.PlayerBar.MOVING_DOWN
		elif event.type == pygame.KEYUP:
			# key raised
			if event.__dict__['key'] == UP_ARROW_KEY and player_bars[MY_PLAYER-1].movement == player_bar.PlayerBar.MOVING_UP:
				player_bars[MY_PLAYER-1].movement = player_bar.PlayerBar.NO_MOVEMENT
			elif event.__dict__['key'] == DOWN_ARROW_KEY and player_bars[MY_PLAYER-1].movement == player_bar.PlayerBar.MOVING_DOWN:
				player_bars[MY_PLAYER-1].movement = player_bar.PlayerBar.NO_MOVEMENT
		elif event.type == pygame.QUIT:
			sys.exit()

	# limit FPS
	clock.tick(MAX_FPS)

	# move players' bars (if needed)
	player_bars[0].move()
	player_bars[1].move()

	# update objects displayed on screen
	screen.fill(SCREEN_BACKGROUND)
	game_ball.update()
	player_bars[0].update()
	player_bars[1].update()
	game_score.update()

	pygame.display.flip()
