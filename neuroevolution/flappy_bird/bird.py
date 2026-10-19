from pathlib import Path

import pygame.draw

from neuroevolution.flappy_bird.brain import Brain

ASSETS = Path(__file__).parent / 'assets'


class Bird:
    _image = None  # loaded once, shared by all birds
    _mask = None
    _rotated = {}  # angle (whole degrees) -> rotated image

    @classmethod
    def _load_image(cls):
        """Loaded on first draw - convert_alpha() needs set_mode() first."""
        image = pygame.image.load(ASSETS / 'bird.png').convert_alpha()
        cls._image = pygame.transform.scale(image, (55, 40))
        cls._mask = pygame.mask.from_surface(cls._image)

    def __init__(self, brain=None):

        self.brain = brain
        if brain is None:
            self.brain = Brain()
        self.fitness = 0
        self.pipes_passed = 0  # pipes this bird passed while alive
        self.alive = True
        self.x = 50
        self.y = 120
        self.velocity = 0
        self.gravity = 0.5
        self.flap_force = -12

    @property
    def image(self):
        if Bird._image is None:
            Bird._load_image()
        return Bird._image

    @property
    def mask(self):
        if Bird._mask is None:
            Bird._load_image()
        return Bird._mask

    def flap(self, height):
        if self.y < height + self.flap_force:
            self.velocity += self.flap_force

    def update(self, height):
        self.velocity += self.gravity
        self.velocity *= 0.95
        self.y += self.velocity
        if self.y > height:
            self.y = height
            self.velocity = 0
        self.fitness += 1

    def _rotated_image(self, tilt_angle):
        angle = int(tilt_angle)  # 1 degree steps look the same and save ~100 rotations per frame
        image = Bird._rotated.get(angle)
        if image is None:
            image = pygame.transform.rotate(self.image, angle)
            Bird._rotated[angle] = image
        return image

    def show(self, screen):
        tilt_angle = -self.velocity * 3
        tilt_angle = max(-90, min(tilt_angle, 25))
        rotated_image = self._rotated_image(tilt_angle)
        rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rotated_rect.topleft)

    def observe(self, next_pipe, height, width):
        """The network inputs - the only place they are defined."""
        return [
            self.y / height,
            self.velocity / height,
            (next_pipe.top - self.y) / height,
            (next_pipe.bottom - self.y) / height,
            (next_pipe.x - self.x) / width
        ]

    def think(self, pipes, height, width):
        """Single bird version. The population decides in one batch,
        see BirdPopulation.update."""
        next_pipe = next((p for p in pipes if p.x + p.w > self.x), None)
        if next_pipe is None:
            return

        flap = self.brain.decide(self.observe(next_pipe, height, width))  # True => Flap
        if flap:
            self.flap(height)

    def crossover(self, partner):
        return self.brain.crossover(self.brain, partner.brain)
