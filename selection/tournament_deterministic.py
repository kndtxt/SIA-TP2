# tournament_deterministic.py

from individual import Individual
from typing import List
from genetic_algorithm import GeneticAlgorithm
import random

def selection_tournament_deterministic(geneticAlgorithm: GeneticAlgorithm, quantity: int) -> List[Individual]:
        """Selección por Torneo Deterministico."""
        tournament_size = 10
        #geneticAlgorithm.calculate_population_fitness(geneticAlgorithm.population)
        picks: List[Individual] = []
        for _ in range(quantity):
            tournament = random.sample(geneticAlgorithm.population, tournament_size)
            picks.append(max(tournament, key=lambda ind: ind.fitness))
        return picks