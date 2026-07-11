import pygame

from settings import *
from game import Game


pygame.init()

screen = pygame.display.set_mode(
    (
        WIDTH,
        HEIGHT
    )
)

pygame.display.set_caption(
    "Ball Arrangement"
)

clock = pygame.time.Clock()

game = Game()

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        game.handle_event(event)



        

    game.update()

    game.draw(screen)

    pygame.display.flip()

pygame.quit()