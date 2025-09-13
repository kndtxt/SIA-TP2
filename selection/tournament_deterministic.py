# tournament_deterministic.py

from individual import Individual
from typing import List
from genetic_algorithm import GeneticAlgorithm
import random

def selection_tournament_deterministic(geneticAlgorithm: GeneticAlgorithm, population: List[Individual], quantity: int, tournament_size: int) -> List[Individual]:
        """Selección por Torneo Deterministico."""
        geneticAlgorithm.calculate_population_fitness(population)
        picks: List[Individual] = []
        for _ in range(quantity):
            tournament = random.sample(population, tournament_size)
            picks.append(max(tournament, key=lambda ind: ind.fitness))
        return picks