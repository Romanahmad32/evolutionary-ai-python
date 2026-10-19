from evolutionary_computing.population import Population
from evolutionary_computing.phrase_finder.phrase_dna import PhraseDna


class PhrasePopulation(Population):
    def __init__(self, target, mutation_rate, population_size):
        super().__init__(mutation_rate)
        self.population = []
        self.target = target
        for i in range(population_size):
            dna = PhraseDna(len(target))
            dna.calculate_fitness(self.target)
            self.population.append(dna)


    def reproduction(self):
        new_population = []
        for i in range(len(self.population)):
            parent_a = self.weighted_selection()
            parent_b = self.weighted_selection()

            child = parent_a.crossover(parent_b)

            child.mutate(self.mutation_rate)
            child.calculate_fitness(self.target)
            new_population.append(child)
        return new_population