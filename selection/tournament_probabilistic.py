# tournament_probabilistic.py

from individual import Individual
from typing import List
from genetic_algorithm import GeneticAlgorithm
import random

def selection_tournament_probabilistic(geneticAlgorithm: GeneticAlgorithm, quantity: int) -> List[Individual]:
        """Selección por Torneo Probabilistico."""
        #geneticAlgorithm.calculate_population_fitness(geneticAlgorithm.population)
        picks: List[Individual] = []
        threshold = 0.9
        for _ in range(quantity):
            r = random.uniform(0, 1)
            tournament = random.sample(geneticAlgorithm.population, 2)
            if r < threshold:
                picks.append(max(tournament, key=lambda ind: ind.fitness))
            else:
                picks.append(min(tournament, key=lambda ind: ind.fitness))
        return picks