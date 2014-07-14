import pygame, sys
from operator import itemgetter

TITLE = "Pong"
TITLE_FONT_SIZE = 90
FONT_SIZE = 50
FONT_COLOR = pygame.Color("#000000")
BG_COLOR = pygame.Color("#CCCCCC")
ONE_PLAYER = 0
QUIT = 1
OPTIONS = { 0: "1 Player", 2: "Quit" }

class StartMenu:
	"""A menu to be popped up at program start and between games."""
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.height = 0
		self.option_rects = []
		self.chosen_option = None

		# allow clicks and quitting the program
		pygame.event.set_allowed(None)
		pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONUP])
	def render(self):
		"""Display the menu."""
		menu_font = pygame.font.Font(None, FONT_SIZE)
		title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
		
		# create title Surface
		title_font.set_bold(True)
		title_surface = title_font.render(TITLE, True, FONT_COLOR)

		# create a Surface for each menu item
		option_surfaces = []
		for key, option_str in sorted(OPTIONS.iteritems(), key=itemgetter(0)):
			option_surface = menu_font.render(option_str, True, FONT_COLOR)
			option_surfaces.append(option_surface)
			self.height += option_surface.get_height()
		items_y = self.screen.get_height() / 2 - self.height / 2

		# render the menu
		self.screen.fill(BG_COLOR)

		self.screen.blit(title_surface, (self.screen.get_width() / 2 - title_surface.get_width() / 2, 30))

		used_height = 0
		for option_surface in option_surfaces:
			x = self.screen.get_width() / 2 - option_surface.get_width() / 2
			y = self.screen.get_height() / 2 - self.height / 2 + used_height
			self.screen.blit(option_surface, (x, y))
			used_height += option_surface.get_height()
			# store rect of surface for event management
			self.option_rects.append(pygame.Rect(x, y, option_surface.get_width(), option_surface.get_height()))

		pygame.display.flip()
	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONUP:
			for i, rect in enumerate(self.option_rects):
				event_x = event.__dict__['pos'][0]
				event_y = event.__dict__['pos'][1]
				if event_x >= rect.left and event_x <= rect.right and event_y >= rect.top and event_y <= rect.bottom:
					self.chosen_option = i
					break
		elif event.type == pygame.QUIT:
			sys.exit()
	def execute(self):
		self.render()
		while self.chosen_option == None:
			# no stalling!
			for event in pygame.event.get():
				self.handle_event(event)
