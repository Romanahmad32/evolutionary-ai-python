import random

from evolutionary_computing.dna import Dna


class FlowerDna(Dna):
    def __init__(self, genes=None):
        super().__init__(genes)
        if genes is None:
            for i in range(14):
                self.genes.append(random.random())

    def crossover(self, partner):
        new_genes = []
        mid_point = random.randint(0, len(self.genes) - 1)
        for i in range(len(self.genes)):
            new_genes.append(self.genes[i] if i > mid_point else partner.genes[i])
        return FlowerDna(new_genes)

    def mutate(self, mutation_rate):
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = random.random()
