
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
    """Selección por Boltzmann."""
    self._calculate_population_fitness()
    exp_fitness = [math.exp(ind.fitness / TEMPERATURE) for ind in self.population]
    total = sum(exp_fitness)
    probabilities = [f / total for f in exp_fitness]
    return random.choices(self.population, weights=probabilities, k=1)[0]
