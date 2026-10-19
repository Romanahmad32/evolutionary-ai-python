import pygame

from evolutionary_computing.interactive_selection.button import Button
from evolutionary_computing.interactive_selection.flower_population import FlowerPopulation

pygame.init()
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive selection")
clock = pygame.time.Clock()
mouse_x, mouse_y = 0, 0
new_gen_button = Button("Evolve new generation", 10, 10, 200, 40)

population = FlowerPopulation(0.05, 10)


def handle_events():
    global population
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN and new_gen_button.check_clicked():
            population.selection()
            population.reproduction()


def draw_flowers():
    global population
    mouse_pos = pygame.mouse.get_pos()
    box_width = WIDTH // 11
    box_height = 200
    draw_x = 0
    for flower in population.population:
        draw_x += box_width
        rect_x = draw_x - (box_width // 2)
        rect_y = (HEIGHT // 2) - 60
        flower_box = pygame.Rect(rect_x,rect_y,box_width,box_height)
        if flower_box.collidepoint(mouse_pos):
            flower.fitness +=1
            pygame.draw.rect(screen,(200,230,200),flower_box)
        else:
            pygame.draw.rect(screen,(240,240,235),flower_box)

        # border
        pygame.draw.rect(screen, (150, 150, 150), flower_box, width=2, border_radius=10)

        flower.show(screen,draw_x,HEIGHT//2)

        my_font = pygame.font.SysFont("Arial", 20)
        fitness_text = my_font.render(f"Fit: {int(flower.fitness)}",True,(0,0,0))
        text_rect = fitness_text.get_rect(center=(draw_x,rect_y+box_height -20))
        screen.blit(fitness_text,text_rect)

while True:
    handle_events()
    screen.fill((225, 225, 220))
    draw_flowers()
    new_gen_button.draw(screen)

    pygame.display.flip()
    clock.tick(60)
