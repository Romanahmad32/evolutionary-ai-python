class Dna:
    def __init__(self, genes=None):
        if genes is None:
            self.genes = []
        else:
            self.genes = genes

    def crossover(self, partner):
        pass

    def mutate(self, mutation_rate):
        pass
