# boltzmann.py
from logging import config
import math
from individual import Individual
from typing import List
import random
from genetic_algorithm import GeneticAlgorithm
import json
import numpy as np

with open('./configs/config.json') as f:
    config = json.load(f)
INITIAL_TEMP = config["boltzmann_initial_temp"]
FINAL_TEMP = config["boltzmann_final_temp"]
DECAY = config["boltzmann_decay"]

def selection_boltzmann(geneticAlgorithm: GeneticAlgorithm, population: List[Individual], quantity: int, generation: int) -> List[Individual]:
    """Selección por Boltzmann.
        Calcula una pseudo aptitud y luego selecciona usando ruleta.
    """
    print("##### fitness dentro de boltzmann ...")
    geneticAlgorithm.calculate_population_fitness(population)
    print("##### Calculando pseudo fitness de Boltzmann...")
    calculate_population_boltzmann_pseudo_fitness(population, generation)
    picks: List[Individual] = []
    while len(picks) < quantity:
        pick = random.uniform(0, 1)
        current = 0.0
        for ind in population:
            current += ind.relative_pseudo_fitness
            if pick <= current:
                picks.append(ind)
                break
    return picks


def calculate_population_boltzmann_pseudo_fitness(population: List[Individual], generation: int):
    """Calcula el pseudo-fitness de boltzman para cada individuo en la población."""
    with open('./configs/config.json') as f:
        config = json.load(f)
    temperature = compute_temperature(INITIAL_TEMP, FINAL_TEMP, DECAY, generation)
    print("##### Temperatura actual: ", temperature)
    total_fitness = 0.0
    max_fitness = 0.0

    for individual in population:
        individual.pseudo_fitness = math.exp(individual.fitness / temperature)
        total_fitness += individual.pseudo_fitness

    avg_fitness = total_fitness / len(population)
    for individual in population:
        individual.relative_pseudo_fitness = individual.pseudo_fitness / avg_fitness
    #primero las individuales
    # for individual in population:
    #     individual.pseudo_fitness = math.exp(individual.fitness / temperature)
    #     total_fitness += individual.pseudo_fitness
    
    # #calculamos el promedio y maximo
    # for individual in population:
    #     individual.pseudo_fitness = individual.pseudo_fitness / total_fitness
    #     if max_fitness < individual.pseudo_fitness:
    #         max_fitness = individual.pseudo_fitness

    # # #calculamos el relativo
    # for individual in population:
    #     # individual.relative_pseudo_fitness = individual.pseudo_fitness / max_fitness
    #     individual.relative_pseudo_fitness = individual.pseudo_fitness 


def compute_temperature(t0: float, tc: float, decay: float, generation: int):
    """Calcula la temperatura en la generación actual."""
    if t0 <= tc:
        return tc
    result = (tc + (t0 - tc)) * np.exp(-decay * generation)
    return result if result > tc else tc