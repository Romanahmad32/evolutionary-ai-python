from types import SimpleNamespace

import numpy as np

from evolutionary_computing.interactive_selection.flower_dna import FlowerDna
from evolutionary_computing.phrase_finder.phrase_dna import PhraseDna
from evolutionary_computing.smart_rockets.rocket_dna import RocketDna
from neuroevolution.flappy_bird.bird_population import BirdPopulation
from neuroevolution.flappy_bird.brain import Brain


def test_flower_genes_keep_their_length():
    dna = FlowerDna()
    for _ in range(10):
        dna = dna.crossover(FlowerDna())
    assert len(dna.genes) == 14


def test_rocket_genes_keep_their_length():
    dna = RocketDna(50)
    for _ in range(10):
        dna = dna.crossover(RocketDna(50))
    assert len(dna.genes) == 50


def test_phrase_fitness():
    dna = PhraseDna(4)
    dna.genes = 'abcd'
    dna.calculate_fitness('abcd')
    assert dna.fitness == 1.0
    dna.calculate_fitness('abxx')
    assert dna.fitness == 0.25


def test_brain_copy_is_independent():
    brain = Brain()
    copy = brain.copy()
    copy.mutate(rate=1.0)
    assert not np.allclose(brain.w1, copy.w1)


def test_batched_decisions_match_single_brains():
    pop = BirdPopulation(population_size=30)
    for i, bird in enumerate(pop.population):
        bird.y = 20 + i * 10
        bird.velocity = i % 7 - 3
    pipe = SimpleNamespace(x=200, w=50, top=150, bottom=250)

    batched = pop.decide_all(pipe, 450, 800)
    single = [bird.brain.decide(bird.observe(pipe, 450, 800)) for bird in pop.population]
    assert list(batched) == single
