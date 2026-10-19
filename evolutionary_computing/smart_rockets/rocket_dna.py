import math
import random

import pygame

from evolutionary_computing.dna import Dna


class RocketDna(Dna):
    def __init__(self, life_span, genes=None):
        super().__init__(genes)
        self.max_force = 0.1
        if genes is None:
            for i in range(life_span):
                angle = random.uniform(0, math.tau)
                force = pygame.Vector2(math.cos(angle), math.sin(angle)) * self.max_force
                self.genes.append(force)

    def crossover(self, partner):
        new_genes = []
        midpoint = random.randint(0, len(self.genes) - 1)
        for i in range(len(self.genes)):
            new_genes.append(self.genes[i] if i > midpoint else partner.genes[i])
        return RocketDna(len(self.genes), new_genes)

    def mutate(self, mutation_rate):
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                angle = random.uniform(0, math.tau)
                self.genes[i] = pygame.Vector2(math.cos(angle), math.sin(angle)) * self.max_force
