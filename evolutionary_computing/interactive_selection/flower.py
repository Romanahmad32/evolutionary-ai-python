import math

import pygame.draw


def map_value(value, start1, stop1, start2, stop2):
    """Map value from the range [start1, stop1] to [start2, stop2]."""
    return start2 + (value - start1) * (stop2 - start2) / (stop1 - start1)


class Flower:
    def __init__(self, dna):
        self.dna = dna
        self.fitness = 1

    def crossover(self, partner):
        return self.dna.crossover(partner.dna)

    def show(self, surface, x, y):
        genes = self.dna.genes
        petal_color = (int(genes[0] * 255), int(genes[1] * 255), int(genes[2] * 255), map_value(genes[3], 0, 1, 120, 255))
        petal_size = map_value(genes[4], 0, 1, 4, 24)
        petal_count = int(map_value(genes[5], 0, 1, 2, 16))
        center_color = (int(genes[6] * 255), int(genes[7] * 255), int(genes[8] * 255))
        center_size = map_value(genes[9], 0, 1, 24, 48)
        stem_color = (int(genes[10] * 255), int(genes[11] * 255), int(genes[12] * 255))
        stem_length = map_value(genes[13], 0, 1, 50, 100)

        pygame.draw.line(surface, stem_color, (x, y), (x, y + stem_length), width=4)

        for i in range(petal_count):
            angle = (i / petal_count) * (2 * math.pi)
            petal_x = x + math.cos(angle) * (center_size / 2)
            petal_y = y + math.sin(angle) * (center_size / 2)

            petal_diameter = int(petal_size * 2)
            petal_surface = pygame.Surface((petal_diameter, petal_diameter), pygame.SRCALPHA)  # transparent petal

            pygame.draw.circle(
                petal_surface,
                petal_color,
                (int(petal_size), int(petal_size)),
                int(petal_size)
            )
            surface.blit(petal_surface, (petal_x - petal_size, petal_y - petal_size))

            pygame.draw.circle(
                surface,
                center_color,
                (int(x), int(y)),
                int(center_size / 2)
            )
