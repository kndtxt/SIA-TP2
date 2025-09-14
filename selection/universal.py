# tournament_universal.py

from individual import Individual
from typing import List
from genetic_algorithm import GeneticAlgorithm
import random

def selection_universal(geneticAlgorithm: GeneticAlgorithm, quantity: int) -> List[Individual]:
        """Selección Universal."""
        if quantity == 0:
            return None
        #geneticAlgorithm.calculate_population_fitness(population)
        picks: List[Individual] = []
        pick = random.uniform(0, 1)
        for k in range(quantity):
            current_pick = (pick + (k-1))/quantity
            current = 0.0
            for ind in geneticAlgorithm.population:
                current += ind.relative_fitness
                if current_pick <= current:
                    picks.append(ind)
                    break
        return picks