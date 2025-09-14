#tournament_deterministic.py
import random
from individual import Individual
from genetic_algorithm import GeneticAlgorithm

def selection_tournament(geneticAlgorithm: GeneticAlgorithm, tournament_size: int = 5) -> Individual:
        """Selección por Torneo."""
        tournament = random.sample(geneticAlgorithm.population, tournament_size)
        return max(tournament, key=lambda ind: ind.fitness)