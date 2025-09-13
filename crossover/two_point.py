# two_point.py

from individual import Individual
import random
import copy
from typing import List

def crossover_two_point(self, parent1: Individual, parent2: Individual) -> List[Individual]:
    """Cruce de dos puntos."""
    child1 = Individual(self.num_triangles, self.width, self.height)
    child2 = Individual(self.num_triangles, self.width, self.height)

    crossover_point1 = random.randint(1, self.num_triangles - 1)
    crossover_point2 = random.randint(crossover_point1, self.num_triangles - 1)

    if crossover_point1 > crossover_point2:
        crossover_point1, crossover_point2 = crossover_point2, crossover_point1

    child1.chromosome = copy.deepcopy(parent1.chromosome[:crossover_point1]
                                       + parent2.chromosome[crossover_point1:crossover_point2]
                                       + parent1.chromosome[crossover_point2:])
    child2.chromosome = copy.deepcopy(parent2.chromosome[:crossover_point1]
                                    + parent1.chromosome[crossover_point1:crossover_point2]
                                    + parent2.chromosome[crossover_point2:])

    return [child1, child2]