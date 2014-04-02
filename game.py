from deck import *

import pygame
import random

# Screen size
(width, height) = (1080, 720)

# Initialize the screen size. The screen variable is the surface we draw
# everything on.
screen = pygame.display.set_mode((width, height))

# Set the title of the game window
pygame.display.set_caption('Kapall')
pygame.font.init()


while True:
	game = Game(screen)
	game.play()
	if not game.replay():
		break

