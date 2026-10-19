import pygame


class Obstacle:
    def __init__(self, x, y, w, h):
        self.position = pygame.Vector2(x, y)
        self.w = w
        self.h = h

    def center(self):
        return pygame.Vector2(self.position.x + (self.w / 2), self.position.y + (self.h / 2))

    def contains(self, spot):
        return spot.x > self.position.x and spot.x < self.position.x + self.w and spot.y > self.position.y and spot.y < self.position.y + self.h
