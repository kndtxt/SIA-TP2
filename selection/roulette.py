# roulette.py

from individual import Individual
from typing import List
from genetic_algorithm import GeneticAlgorithm
import random

def selection_roulette(geneticAlgorithm: GeneticAlgorithm, quantity: int) -> List[Individual]:
    """Selección por Ruleta."""
    #geneticAlgorithm.calculate_population_fitness(population)
    picks: List[Individual] = []
    current = 0.0
    for _ in range(quantity):
        pick = random.uniform(0, 1)
        for ind in geneticAlgorithm.population:
            current += ind.relative_fitness
            if pick <= current:
                picks.append(ind)
                break
    return picks