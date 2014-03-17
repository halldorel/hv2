import pygame
import random

# Background color (duh!)
background_color = (80, 170, 80)

# Screen size
(width, height) = (1080, 720)

# Initialize the screen size. The screen variable is the surface we draw
# everything on.
screen = pygame.display.set_mode((width, height))

# Set the title of the game window
pygame.display.set_caption('Kapall')

# The game is running.
running = True

# First thing first, load our hero
bjorundur = pygame.image.load('bjorundur.png')

# Makeshift 'Card' class implementation. To be merged with the real one.
class Card:
	def __init__(self, x, y):
		self.pos = (x, y)
		self.size = (150, 190)
		self.rect = pygame.Rect(self.pos, self.size)
		self.surf = pygame.Surface(self.size)
		self.surf.blit(bjorundur, (-20,-20))

	# Draw the card at current pos. blit stands for 'block image transfer'
	# and basically means 'print this on that', this being our card and
	# that being our screen
	def draw(self, screen):
		screen.blit(self.surf, self.pos)

	def nudge(self, delta):
		self.pos = (self.pos[0] + delta[0], self.pos[1] + delta[1])
		self.rect = pygame.Rect(self.pos, self.size)

	def __repr__(self):
		return str(self.pos) + " " + str(self.size)

# The card held by the user. Is set to None if mouse is up
current_card = None

spilastokkur = [Card(20+180*x, 20+220*y) for x in range(3) for y in range(3)]

# Check which card is pressed. Returns None if no card is pressed.
def card_pressed(mouse_pos):
	# Search for card in reversed list. Cards appearing later in list
	# have precedence as they are rendered last and thus appear on top.
	for card in spilastokkur[::-1]:
		if card.rect.collidepoint(mouse_pos):
			# Newly moved cards are put in front
			spilastokkur.remove(card)
			spilastokkur.append(card)
			return card
	return None

# Main game loop
while running:

	# Each time, we draw all the components of the screen, beginning
	# with the background. We draw the background by filling the 'screen'
	# surface with a solid color.
	screen.fill(background_color)

	# Loop through the event queue to check what's happening.
	for event in pygame.event.get():
		# Voluntary quit
		if event.type == pygame.QUIT:
			running = False
		# Release the card currently held, when releasing the mouse
		if event.type == pygame.MOUSEBUTTONUP:
			if current_card:
				current_card = None

	# Mouse event variables.
	mouse_buttons = pygame.mouse.get_pressed()
	mouse_delta = pygame.mouse.get_rel()
	mouse_pos = pygame.mouse.get_pos()

	# If left mouse button is pressed, check if we're holding a card
	# if not, holding a card, set current_card to the card pressed
	if mouse_buttons == (1, 0, 0):
		if not current_card:
			current_card = card_pressed(mouse_pos)
		else:
			current_card.nudge(mouse_delta)

	# Loop through all the cards, and draw then on our screen. Cards
	# drawn last are drawn on top of other cards, so this time we
	# run through the list from the beginning to the end.
	for card in spilastokkur:
		card.draw(screen)

	# Update the screen.
	pygame.display.flip()