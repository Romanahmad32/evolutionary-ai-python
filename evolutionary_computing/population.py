import random


class Population:
    def __init__(self, mutation_rate):
        self.mutation_rate = mutation_rate
        self.generation = 0
        self.population = []

    def weighted_selection(self):
        total_fitness = sum(ind.fitness for ind in self.population)

        if total_fitness == 0:
            return random.choice(self.population)

        start = random.uniform(0, total_fitness)
        index = 0

        while start > 0 and index < len(self.population):
            start -= self.population[index].fitness
            index += 1

        index = max(0, index - 1)
        return self.population[index]

    def reproduction(self):
        pass
