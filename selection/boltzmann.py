# boltzmann.py
import math
from individual import Individual
from typing import List
import random
from genetic_algorithm import GeneticAlgorithm

TEMPERATURE = 0
  
def selection_boltzmann(geneticAlgorithm: GeneticAlgorithm, population: List[Individual], quantity: int) -> Individual:
    """Selección por Boltzmann.
        Calcula una pseudo aptitud y luego selecciona usando ruleta.
    """
    geneticAlgorithm.calculate_population_fitness(population)
    calculate_population_boltzmann_pseudo_fitness(population)
    picks: List[Individual] = []
    for _ in range(quantity):
        pick = random.uniform(0, 1)
        current = 0.0
        for ind in population:
            current += ind.relative_pseudo_fitness
            if pick <= current:
                picks.append(ind)
                break
    return picks


def calculate_population_boltzmann_pseudo_fitness(population: List[Individual]):
    """Calcula el pseudo-fitness de boltzman para cada individuo en la población."""
    total_fitness = 0.0
    max_fitness = 0.0
    #primero las individuales
    for individual in population:
        individual.pseudo_fitness = math.exp(individual.fitness / TEMPERATURE)
        total_fitness += individual.pseudo_fitness
    
    #calculamos el promedio y maximo
    for individual in population:
        individual.pseudo_fitness = individual.pseudo_fitness / total_fitness
        if max_fitness < individual.pseudo_fitness:
            max_fitness = individual.pseudo_fitness

    #calculamos el relativo
    for individual in population:
        individual.relative_pseudo_fitness = individual.pseudo_fitness / max_fitness