import numpy as np
from matplotlib import pyplot as plt

from evolutionary_computing.phrase_finder.phrase_population import PhrasePopulation

if __name__ == '__main__':
    max_generations = 10000
    mutation_rate = 0.01
    population_size = 250
    target = "to be or not to be that is the question ok"

    pop = PhrasePopulation(target, mutation_rate, population_size)
    target_found = False
    generations = np.array([])
    average_fitness = np.array([])
    while (pop.generation < max_generations) and not target_found:
        best_phrase = ''

        for i in range(len(pop.population)):
            if pop.population[i].fitness >= 1.0:
                target_found = True
                print('Target found')
                break
        current_average_fitness = sum(p.fitness for p in pop.population) / len(pop.population)
        best_phrase = max(pop.population, key=lambda p: p.fitness)
        pop.population = pop.reproduction()
        print('-------------------')
        print(f'{best_phrase}\naverage_fitness: {current_average_fitness}\ngeneration: {pop.generation}')

        pop.generation += 1
        generations = np.append(generations, pop.generation)
        average_fitness = np.append(average_fitness, current_average_fitness)

    plt.plot(generations, average_fitness)
    plt.xlabel('Generations')
    plt.ylabel('Average Fitness')
    plt.title('Fitness over generations')
    plt.grid(True)
    plt.show()
