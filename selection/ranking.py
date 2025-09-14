# ranking.py

from individual import Individual
from typing import List
from genetic_algorithm import GeneticAlgorithm
import random

def calculate_population_ranking_pseudo_fitness(geneticAlgorithm: GeneticAlgorithm):
    """Calcula el pseudo-fitness de ranking para cada individuo en la población."""
    #geneticAlgorithm.calculate_population_fitness(population)
    sorted_population = sorted(geneticAlgorithm.population, key=lambda ind: ind.fitness, reverse=True)
    n = len(sorted_population)

    total_fitness = 0.0
    for rank, individual in enumerate(sorted_population):
        individual.pseudo_fitness = (n - (rank + 1)) / n
        total_fitness += individual.pseudo_fitness

    for individual in sorted_population:
        individual.relative_pseudo_fitness = individual.pseudo_fitness / total_fitness

def selection_ranking(geneticAlgorithm: GeneticAlgorithm, quantity: int) -> List[Individual]:
    """Selección por Ranking."""
    calculate_population_ranking_pseudo_fitness(geneticAlgorithm, geneticAlgorithm.population)
    picks: List[Individual] = []
    pick = random.uniform(0, 1)
    current = 0.0
    for _ in range(quantity):
        for ind in geneticAlgorithm.population:
            current += ind.relative_pseudo_fitness
            if pick <= current:
                picks.append(ind)
                break
    return picks