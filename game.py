from deck import *
import pygame

background_color = (250, 250, 250)
(width, height) = (1080, 720)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Kapall')
screen.fill(background_color)

pygame.display.flip()

deck = deck()
print deck
running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False