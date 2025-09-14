# elitist.py

from individual import Individual
import math
from typing import List
from genetic_algorithm import GeneticAlgorithm

def selection_elitist(geneticAlgorithm: GeneticAlgorithm, population: List[Individual], quantity: int) -> List[Individual]:
        """Selección por Elitista."""
        geneticAlgorithm.calculate_population_fitness(population)
        pop_size = len(population)
        population.sort(key=lambda ind: ind.fitness, reverse=True) #de mejor a peor
        picks: List[Individual] = []
        idx = 0
        for ind in population:
            if idx >= quantity:
                break
            count = math.ceil(quantity - idx / pop_size) #cuantas veces elegimos a ese individuo
            while len(picks) < count:
                if idx >= quantity:
                    break
                picks.append(ind)
                idx += 1
        return picks