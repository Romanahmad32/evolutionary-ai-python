import random
import string

from evolutionary_computing.dna import Dna


class PhraseDna(Dna):
    def __init__(self, length):
        super().__init__(''.join(random.choices(string.ascii_lowercase + ' ', k=length)))
        self.fitness = 0

    def __str__(self):
        return self.genes

    def calculate_fitness(self, target):
        if len(target) != len(self.genes):
            return
        score = 0

        for i in range(len(self.genes)):
            if self.genes[i] == target[i]: score += 1
        self.fitness = (score / len(target))**2

    def crossover(self, partner):
        child = PhraseDna(len(self.genes))
        midpoint = random.choice(range(len(self.genes)))
        child.genes = self.genes[:midpoint] + partner.genes[midpoint:]
        return child

    def mutate(self, mutation_rate):
        genes_list = list(self.genes)

        for i in range(len(genes_list)):
            if random.random() < mutation_rate:
                genes_list[i] = random.choice(string.ascii_lowercase + ' ')

        self.genes = ''.join(genes_list)
