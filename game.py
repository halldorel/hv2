from deck import *

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

pygame.font.init()

# The game is running.
running = True

# First thing first, load our hero
BJORUNDUR = pygame.image.load('bjorundur.png')

# The card held by the user. Is set to None if mouse is up
current_card = None

game = Game()
game.draw()

game.draw()
game.draw()
game.draw()

# Main game loop

# TODO: Move mainloop inside of Game class.
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
			current_card = game.card_pressed(mouse_pos)
		else:
			current_card.nudge(mouse_delta)

	# Loop through all the cards, and draw then on our screen. Cards
	# drawn last are drawn on top of other cards, so this time we
	# run through the list from the beginning to the end.

	game.render(screen);

	# TODO: Merge this to main gameloop
	if current_card:
		current_card.render(screen)

	# Update the screen.
	pygame.display.flip()