import pickle
import sys
from pathlib import Path

import keras.models
import numpy as np
import pygame

WIDTH, HEIGHT = 640, 240
HERE = Path(__file__).parent

# Load model and encoder
model = keras.models.load_model(HERE / 'gesture_model.keras')
with open(HERE / 'label_encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture detector")
clock = pygame.time.Clock()
start_x, start_y = 0, 0
end_x, end_y = 0, 0
vector_x, vector_y = 0, 0
show_prediction = False
prediction = None


def handle_events():
    global show_prediction, prediction, start_x, start_y, vector_x, vector_y, end_x, end_y
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            start_x, start_y = pos
            show_prediction = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            end_x, end_y = pos
            show_prediction = True
            vector_x = end_x - start_x
            vector_y = end_y - start_y

            # letting model predict
            input_data = np.array([[vector_x, vector_y]])
            prediction_probs = model.predict(input_data, verbose=0)
            probs = prediction_probs[0]
            print('-- Model probabilities --')
            for label, prob in zip(encoder.classes_, probs):
                print(f'{label}: {prob * 100:.2f}%')
            best_index = np.argmax(prediction_probs)
            prediction = encoder.classes_[best_index]

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            end_x, end_y = pos


def draw():
    global screen, show_prediction, prediction
    if (start_x, start_y) != (0, 0) and (end_x, end_y) != (0, 0):
        pygame.draw.line(screen, (0, 0, 0), start_pos=(start_x, start_y), end_pos=(end_x, end_y), width=5)
    if show_prediction:
        font = pygame.font.SysFont(None, 48)
        text_surface = font.render(prediction, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(300, 200))
        screen.blit(text_surface, text_rect)


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
