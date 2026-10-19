import sys

import pygame

from evolutionary_computing.smart_rockets.obstacle import Obstacle
from evolutionary_computing.smart_rockets.rocket_population import RocketPopulation

WIDTH, HEIGHT = 640, 240
LIFE_SPAN = 290  # how long each generation lives, in frames
POP_SIZE = 300
MUTATION_RATE = 0.01

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Rockets")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)
obstacle = Obstacle(WIDTH/2 - 50, HEIGHT /2, 100, 15)
target = Obstacle(WIDTH / 2 - 13, 24,27,27)
population = RocketPopulation(POP_SIZE, LIFE_SPAN, WIDTH / 2, HEIGHT - 10, MUTATION_RATE)
life_counter = 0


def draw():
    global life_counter

    screen.fill((255, 255, 255))  # background(255)

    # draw the target
    pygame.draw.rect(screen, (127, 127, 127), (int(target.position.x), int(target.position.y),int(target.w),int(target.h)))

    # draw an obstacle
    pygame.draw.rect(screen, (127, 127, 127),
                     (int(obstacle.position.x), int(obstacle.position.y), int(obstacle.w),int(obstacle.h)))

    if life_counter < LIFE_SPAN:
        population.live(target, WIDTH, HEIGHT, [obstacle])
        life_counter += 1
    else:
        life_counter = 0
        population.fitness(target)
        population.selection()
        population.reproduction()

    population.draw(screen)

    info = f"Generation #: {population.generation}    Cycles left: {LIFE_SPAN - life_counter}"
    screen.blit(font.render(info, True, (0, 0, 0)), (10, 10))

    pygame.display.flip()


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:

            target.position.x, target.position.y = event.pos


def main():
    while True:
        handle_events()
        draw()
        clock.tick(60)


if __name__ == "__main__":
    main()
