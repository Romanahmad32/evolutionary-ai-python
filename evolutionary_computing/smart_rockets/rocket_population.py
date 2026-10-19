import random

from evolutionary_computing.population import Population
from evolutionary_computing.smart_rockets.rocket import Rocket
from evolutionary_computing.smart_rockets.rocket_dna import RocketDna


class RocketPopulation(Population):
    def __init__(self, size, life_span, start_x, start_y, mutation_rate):
        super().__init__(mutation_rate)
        self.population = []
        self.start_x = start_x
        self.start_y = start_y

        for i in range(size):
            self.population.append(Rocket(start_x, start_y, RocketDna(life_span)))

    def weighted_selection(self):
        index = 0
        start = random.random()

        while start > 0 and index < len(self.population):
            start -= self.population[index].fitness
            index += 1
        index = max(0, index - 1)
        return self.population[index]

    def fitness(self, target):
        for rocket in self.population:
            rocket.calculate_fitness(target)

    def selection(self):
        total_fitness = sum(rocket.fitness for rocket in self.population)
        if total_fitness == 0:
            total_fitness = 1
        for rocket in self.population:
            rocket.fitness /= total_fitness

    def reproduction(self):
        new_population = []
        for i in range(len(self.population)):
            parent_a = self.weighted_selection()
            parent_b = self.weighted_selection()

            child = parent_a.crossover(parent_b)
            child.mutate(self.mutation_rate)
            new_population.append(Rocket(self.start_x, self.start_y, child))
        self.population = new_population
        self.generation += 1

    def live(self, target, width, height, obstacles):
        for rocket in self.population:
            rocket.run(target, width, height, obstacles)

    def draw(self, screen):
        for rocket in self.population:
            rocket.draw(screen)
