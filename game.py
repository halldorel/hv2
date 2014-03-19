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
last_table = None

game = Game()

# Main game loop

# TODO: Move mainloop inside of Game class.
while running:
	# Each time, we draw all the components of the screen, beginning
	# with the background. We draw the background by filling the 'screen'
	# surface with a solid color.
	screen.fill(background_color)

	# Loop through the event queue to check what's happening.
	for event in pygame.event.get():
		# Mouse event variables.
		mouse_buttons = pygame.mouse.get_pressed()
		mouse_delta = pygame.mouse.get_rel()
		mouse_pos = pygame.mouse.get_pos()
	
		# Voluntary quit
		if event.type == pygame.QUIT:
			running = False	

		# Release the card if currently held, when releasing the mouse
		if event.type == pygame.MOUSEBUTTONUP:
			if current_card and last_table:
				if not game.handle_card_dropped(current_card):
					last_table.place(current_card)
				current_card = None
		if event.type == pygame.MOUSEBUTTONDOWN:
			game.handle_draw(mouse_pos)

		# If left mouse button is pressed, check if we're holding a card
		# if not, holding a card, set current_card to the card pressed
		if mouse_buttons == (1, 0, 0):
			if not current_card:
				if game.card_pressed(mouse_pos):
					(current_card, last_table) = game.card_pressed(mouse_pos)
					if current_card and last_table:
						print current_card
						print last_table
						current_card = last_table.top()
						last_table.pop();
			else:
				current_card.nudge(mouse_delta)

	game.render(screen);

	# TODO: Merge this to main gameloop
	if current_card and not current_card.is_dummy():
		print "dragging" + str(current_card)
		current_card.render(screen)

	# Update the screen.
	pygame.display.flip()