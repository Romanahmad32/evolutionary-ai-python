import random

from evolutionary_computing.interactive_selection.flower import Flower
from evolutionary_computing.interactive_selection.flower_dna import FlowerDna
from evolutionary_computing.population import Population


class FlowerPopulation(Population):
    def __init__(self, mutation_rate, size=10):
        super().__init__(mutation_rate)
        self.population = []
        for i in range(size):
            self.population.append(Flower(FlowerDna()))

    def weighted_selection(self):
        index = 0
        start = random.random()
        while start > 0 and index < len(self.population):
            start -= self.population[index].fitness
            index += 1
        index = max(0, index - 1)
        return self.population[index]

    def selection(self):
        total_fitness = sum(flower.fitness for flower in self.population)
        if total_fitness == 0:
            total_fitness = 1
        for flower in self.population:
            flower.fitness /= total_fitness

    def reproduction(self):
        new_population = []
        for i in range(len(self.population)):
            parent_a = self.weighted_selection()
            parent_b = self.weighted_selection()

            child = parent_a.crossover(parent_b)
            child.mutate(self.mutation_rate)
            new_population.append(Flower(child))
        self.population = new_population
        self.generation += 1
