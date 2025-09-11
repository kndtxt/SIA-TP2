
import random
from individual import Individual
import random
import copy
from typing import List
import json
import math

TEMPERATURE = 0
with open('run_config.json', 'r') as f:
    config = json.load(f)
    TEMPERATURE = config.get("boltzmann", {}).get("temperature", TEMPERATURE)

def selection_boltzmann(self) -> Individual:
    """Selección por Boltzmann.
        Calcula una pseudo aptitud y luego selecciona usando ruleta.
    """
    calculate_population_boltzmann_pseudo_fitness(self)
    pick = random.uniform(0, 1)
    current = 0.0
    for ind in self.population:
        current += ind.relative_pseudo_fitness
        if pick <= current:
            return ind


def calculate_population_boltzmann_pseudo_fitness(self):
    """Calcula el pseudo-fitness de boltzman para cada individuo en la población."""
    total_fitness = 0.0
    max_fitness = 0.0
    #primero las individuales
    for individual in self.population:
        individual.pseudo_fitness = math.exp(individual.fitness / TEMPERATURE)
        total_fitness += individual.pseudo_fitness
    
    #calculamos el promedio y maximo
    for individual in self.population:
        individual.pseudo_fitness = individual.pseudo_fitness / total_fitness
        if max_fitness < individual.pseudo_fitness:
            max_fitness = individual.pseudo_fitness

    #calculamos el relativo
    for individual in self.population:
        individual.relative_pseudo_fitness = individual.pseudo_fitness / max_fitness