import pygame, sys
import traits

from pygame.locals import *

pygame.init()

SCREEN = pygame.display.set_mode((300,300))

pygame.display.set_caption('Game of Life')

def generate_agents():
    # pos = (100,50,20,20)
    # rad = 20
    # pygame.draw.circle(SCREEN , (0,255,0), (100,50), rad)
    agent = traits.Organism()
    pygame.draw.circle(SCREEN, agent.color, (100,50), agent.size)

generate_agents()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
