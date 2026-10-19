import csv
import sys
from pathlib import Path

import pygame

WIDTH, HEIGHT = 640, 240
DATA_FILE = Path(__file__).parent / 'gesture_data.csv'

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture data collection")
clock = pygame.time.Clock()
start_x, start_y = 0, 0
end_x, end_y = 0, 0
vector_x, vector_y = 0, 0

training_data = []
current_label = "up"  # default label at start


def handle_events():
    global start_x, start_y, vector_x, vector_y, end_x, end_y
    global current_label, training_data

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # arrow keys choose the label, S saves
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current_label = "up"
                print("Mode: UP")
            elif event.key == pygame.K_DOWN:
                current_label = "down"
                print("Mode: DOWN")
            elif event.key == pygame.K_LEFT:
                current_label = "left"
                print("Mode: LEFT")
            elif event.key == pygame.K_RIGHT:
                current_label = "right"
                print("Mode: RIGHT")
            elif event.key == pygame.K_s:
                save_to_csv()

        # mouse down: start point
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_x, start_y = pygame.mouse.get_pos()
            end_x, end_y = (0, 0)

        # mouse up: end point, record the sample
        if event.type == pygame.MOUSEBUTTONUP:
            end_x, end_y = pygame.mouse.get_pos()
            vector_x = end_x - start_x
            vector_y = end_y - start_y

            # skip zero vectors (click without dragging)
            if vector_x != 0 or vector_y != 0:
                training_data.append({
                    "vector_x": vector_x,
                    "vector_y": vector_y,
                    "label": current_label
                })
                print(f"Recorded: {current_label} -> ({vector_x}, {vector_y})")


def save_to_csv():
    if not training_data:
        print("No data to save.")
        return

    with open(DATA_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["vector_x", "vector_y", "label"])
        writer.writeheader()
        writer.writerows(training_data)

    print(f"Saved {len(training_data)} samples to {DATA_FILE.name}")


def draw():
    if (start_x, start_y) != (0, 0) and (end_x, end_y) != (0, 0):
        pygame.draw.line(screen, (0, 0, 0), start_pos=(start_x, start_y), end_pos=(end_x, end_y), width=5)


def main():
    global screen
    while True:
        screen.fill("grey")
        handle_events()
        draw()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
