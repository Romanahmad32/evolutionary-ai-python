import random
from pathlib import Path

import pygame

ASSETS = Path(__file__).parent / 'assets'


class Pipe:
    SCALE = 2.5  # scale factor for the pixel art sprites

    _cap = None   # loaded once, shared by all pipes
    _body = None

    @classmethod
    def _load_images(cls):
        cap = pygame.image.load(ASSETS / 'pipe_cap.png').convert_alpha()
        body = pygame.image.load(ASSETS / 'pipe_body.png').convert_alpha()
        cls._cap = pygame.transform.scale_by(cap, cls.SCALE)
        cls._body = pygame.transform.scale_by(body, cls.SCALE)

    @classmethod
    def _build(cls, length):
        """Cap at a fixed size, body stretched to the given length."""
        cap_w, cap_h = cls._cap.get_size()
        body_w = cls._body.get_width()
        surface = pygame.Surface((cap_w, max(length, cap_h)), pygame.SRCALPHA)
        body_h = surface.get_height() - cap_h
        if body_h > 0:
            stretched = pygame.transform.scale(cls._body, (body_w, body_h))
            surface.blit(stretched, ((cap_w - body_w) // 2, cap_h))
        surface.blit(cls._cap, (0, 0))
        return surface

    def __init__(self, width, height):
        if Pipe._cap is None:
            Pipe._load_images()
        self.passed = False
        self.spacing = 100
        self.w = Pipe._body.get_width()  # collision width = body width
        margin = 40
        self.top = random.randint(margin, height - self.spacing - margin)
        self.bottom = self.top + self.spacing
        self.x = width
        self.velocity = 2

        self.image_bottom = Pipe._build(height - self.bottom)
        self.image_top = pygame.transform.flip(Pipe._build(self.top), False, True)

        self.mask_top = pygame.mask.from_surface(self.image_top)
        self.mask_bottom = pygame.mask.from_surface(self.image_bottom)

        self.draw_offset = (self.image_bottom.get_width() - self.w) // 2

    def show(self, screen, height):
        x = self.x - self.draw_offset
        screen.blit(self.image_top, (x, self.top - self.image_top.get_height()))
        screen.blit(self.image_bottom, (x, self.bottom))

    def update(self):
        self.x -= self.velocity

    def collides(self, bird):
        vertical_collision = bird.y < self.top or bird.y > self.bottom
        horizontal_collision = self.x < bird.x < self.x + self.w
        return vertical_collision and horizontal_collision

    def offscreen(self):
        return self.x <= -self.w
