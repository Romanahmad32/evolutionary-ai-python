import random

import numpy as np

from neuroevolution.flappy_bird.bird import Bird


class BirdPopulation:
    PIPE_WEIGHT = 1000  # one passed pipe is worth as much as 1000 frames

    def __init__(self, mutation_rate=0.01, population_size=20):
        self.mutation_rate = mutation_rate
        self.generation = 0
        self.population = []
        self.history = []  # one row per finished generation
        for i in range(population_size):
            self.population.append(Bird())
        self._stack_brains()

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

    def living_birds(self):
        count = 0
        for bird in self.population:
            if bird.alive:
                count += 1
        return count

    def normalize_fitness(self):
        total = 0
        for bird in self.population:
            total += bird.fitness
        for bird in self.population:
            if total != 0:
                bird.fitness /= total
            bird.fitness = pow(bird.fitness, 2)

    def reproduction(self):
        new_population = [Bird(self.best_bird().brain.copy())]
        for i in range(len(self.population)-1):
            parent_a = self.weighted_selection()
            parent_b = self.weighted_selection()

            child = parent_a.crossover(parent_b)
            child.mutate(self.mutation_rate)
            new_population.append(Bird(child))
        self.population = new_population
        self.generation += 1
        self._stack_brains()

    def show(self, screen):
        for bird in self.population:
            if bird.alive:
                bird.show(screen)

    def _stack_brains(self):
        """Stack all brains into one array per layer - allows a single
        matmul for the whole population instead of N tiny numpy calls."""
        brains = [bird.brain for bird in self.population]
        self.W1 = np.stack([b.w1 for b in brains])  # (N, inputs, hidden)
        self.B1 = np.stack([b.b1 for b in brains])  # (N, hidden)
        self.W2 = np.stack([b.w2 for b in brains])  # (N, hidden, outputs)
        self.B2 = np.stack([b.b2 for b in brains])  # (N, outputs)

    def decide_all(self, next_pipe, height, width):
        """One forward pass for the whole population. True = flap."""
        x = np.array([bird.observe(next_pipe, height, width) for bird in self.population])
        hidden = np.maximum(0.0, np.einsum('ni,nih->nh', x, self.W1) + self.B1)  # ReLU
        output = np.einsum('nh,nho->no', hidden, self.W2) + self.B2
        return output[:, 0] > output[:, 1]

    def pipe_passed(self):
        """A pipe was passed - counts for every bird that is still alive."""
        for bird in self.population:
            if bird.alive:
                bird.pipes_passed += 1

    def apply_fitness_weights(self):
        """Every bird gets the time until the first pipe for free; it carries
        no information and would only hide the differences. So fitness is
        relative to the worst bird, and passed pipes are weighted heavily."""
        base = min(bird.fitness for bird in self.population)
        for bird in self.population:
            bird.fitness = self.PIPE_WEIGHT * bird.pipes_passed + (bird.fitness - base)

    def record_stats(self):
        """Must run before normalize_fitness - the raw fitness is gone after that."""
        fitness = [bird.fitness for bird in self.population]
        pipes = [bird.pipes_passed for bird in self.population]
        self.history.append({
            'generation': self.generation,
            'best_fitness': max(fitness),
            'mean_fitness': sum(fitness) / len(fitness),
            'mean_pipes': sum(pipes) / len(pipes),
        })

    def update(self, pipes, height, width):
        # All birds share the same x: next_pipe is the same for all of them,
        # and it is the only pipe that can be hit.
        bird_x = self.population[0].x
        next_pipe = next((p for p in pipes if p.x + p.w > bird_x), None)
        if next_pipe is None:
            return False

        flaps = self.decide_all(next_pipe, height, width)
        for bird, flap in zip(self.population, flaps):
            if not bird.alive:
                continue
            if flap:
                bird.flap(height)
            bird.update(height)
            if next_pipe.collides(bird):
                bird.alive = False

        if self.all_birds_dead():
            self.record_stats()  # raw frames, before any weighting
            self.apply_fitness_weights()
            self.normalize_fitness()
            self.reproduction()
            return True
        return False

    def all_birds_dead(self):
        for bird in self.population:
            if bird.alive:
                return False
        return True

    def best_bird(self):
        return max(self.population, key=lambda bird: bird.fitness)
