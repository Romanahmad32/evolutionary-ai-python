import csv
import sys
from pathlib import Path

import pygame

from neuroevolution.flappy_bird.bird_population import BirdPopulation
from neuroevolution.flappy_bird.pipe import Pipe

WIDTH, HEIGHT = 800, 450
PIPE_SPACING = 220
FAST_STEPS = 200  # simulation steps per drawn frame in fast mode

HERE = Path(__file__).parent
METRICS_FILE = HERE / 'metrics.csv'
METRICS_FIELDS = ['generation', 'score', 'highscore', 'best_fitness', 'mean_fitness', 'mean_pipes']

render = True

pygame.init()
bg = pygame.image.load(HERE / 'assets' / 'background.png')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

pop = BirdPopulation(population_size=100)
pipes = []
BIRD_X = pop.population[0].x  # all birds share the same x position
score = 0                     # pipes passed in this generation
highscore = 0                 # best score over all generations


def reset_pipes():
    global score
    pipes.clear()
    score = 0
    for i in range(4):
        pipes.append(Pipe(WIDTH + PIPE_SPACING * i, HEIGHT))


def update_pipes():
    global score, highscore
    for pipe in pipes:
        pipe.update()
        if not pipe.passed and pipe.x + pipe.w < BIRD_X:
            pipe.passed = True
            score += 1
            highscore = max(highscore, score)
            pop.pipe_passed()
    if pipes[0].offscreen():
        pipes.pop(0)
    if pipes[-1].x <= WIDTH - PIPE_SPACING:  # spacing instead of a frame counter
        pipes.append(Pipe(WIDTH, HEIGHT))


def start_metrics():
    with open(METRICS_FILE, 'w', newline='') as f:
        csv.DictWriter(f, METRICS_FIELDS).writeheader()


def record_generation():
    """Add the score to the stats of the generation that just ended and
    write it right away - so the curve survives an interrupted run."""
    row = dict(pop.history[-1], score=score, highscore=highscore)
    with open(METRICS_FILE, 'a', newline='') as f:
        csv.DictWriter(f, METRICS_FIELDS).writerow(row)


def step():
    update_pipes()
    if pop.update(pipes, HEIGHT, WIDTH):
        record_generation()
        reset_pipes()


def handle_events():
    global render
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                render = not render


def draw_hud():
    mode = "Render" if render else f"Fast x{FAST_STEPS}"
    lines = [
        f'Gen: {pop.generation}   Alive: {pop.living_birds()}/{len(pop.population)}   [Space] {mode}',
        f'Score: {score}   Highscore: {highscore}',
    ]
    for i, line in enumerate(lines):
        screen.blit(font.render(line, True, (255, 255, 255)), (10, 10 + i * 26))


def draw():
    screen.blit(bg, (0, 0))
    if render:
        for pipe in pipes:
            pipe.show(screen, HEIGHT)
        pop.show(screen)
    draw_hud()
    pygame.display.flip()


def main():
    start_metrics()
    reset_pipes()
    while True:
        handle_events()
        for _ in range(1 if render else FAST_STEPS):
            step()
        draw()
        clock.tick(60 if render else 0)


if __name__ == "__main__":
    main()
