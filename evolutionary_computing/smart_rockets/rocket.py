import math

import pygame


class Rocket:
    def __init__(self, x, y, dna):
        self.record_distance = float('inf')
        self.hit_obstacle = False
        self.hit_target = False
        self.fitness = 0
        self.dna = dna
        self.gene_counter = 0
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.crashed = False
        self.finish_counter = 0

    def run(self, target, width, height, obstacles):
        if self.hit_target or self.crashed:
            return
        if self.gene_counter < len(self.dna.genes) and not self.hit_obstacle:
            self.apply_force(self.dna.genes[self.gene_counter])
            self.gene_counter += 1
            self.update()
            self.check_target(target)
            self.check_edges(width, height)
            self.check_obstacles(obstacles)
        if not self.hit_target:
            self.finish_counter += 1

    def check_obstacles(self, obstacles):
        for obstacle in obstacles:
            if obstacle.contains(self.position):
                self.hit_obstacle = True

    def apply_force(self, force):
        self.acceleration += force

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0

    def check_target(self, target):
        distance = self.position.distance_to(target.center())
        if distance < self.record_distance:
            self.record_distance = distance
        if target.contains(self.position):
            self.hit_target = True

    def check_edges(self, width, height):
        if not (0 <= self.position.x <= width and 0 <= self.position.y <= height):
            self.crashed = True

    def calculate_fitness(self, target):
        self.fitness = (1 / (self.record_distance + 1)) ** 4
        if self.hit_target:
            self.fitness *= 10 / (self.finish_counter + 1)  # time only matters if you arrived
        if self.crashed or self.hit_obstacle:
            self.fitness *= 0.1

    def crossover(self, partner):
        return self.dna.crossover(partner.dna)

    def mutate(self, mutation_rate):
        self.dna.mutate(mutation_rate)

    def draw(self, screen):
        color = (60, 60, 60)
        if self.hit_target:
            color = (0, 160, 0)
        elif self.crashed:
            color = (200, 0, 0)

        if self.velocity.length_squared() > 0:
            angle = math.atan2(self.velocity.y, self.velocity.x)
        else:
            angle = -math.pi / 2

        # Small triangle pointing in the direction of travel
        length = 8
        tip = self.position + pygame.Vector2(math.cos(angle), math.sin(angle)) * length
        left = self.position + pygame.Vector2(math.cos(angle + 2.5), math.sin(angle + 2.5)) * (length * 0.6)
        right = self.position + pygame.Vector2(math.cos(angle - 2.5), math.sin(angle - 2.5)) * (length * 0.6)
        pygame.draw.polygon(screen, color, [tip, left, right])
