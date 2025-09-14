#roulette.py
import random
from individual import Individual

def selection_roulette(population) -> Individual:
        """Selección por Ruleta."""
        total_fitness = sum(ind.fitness for ind in population)
        pick = random.uniform(0, total_fitness)
        current = 0
        for ind in population:
            current += ind.fitness
            if current > pick:
                return ind
        return population[-1]