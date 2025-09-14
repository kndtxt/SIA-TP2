# two_point.py

from individual import Individual
import random
import copy
from typing import List
from genetic_algorithm import GeneticAlgorithm

def crossover_two_point(geneticAlgorithm: GeneticAlgorithm, parents:List[Individual]) -> List[Individual]:
    """Cruce de dos puntos."""
    children = []

    for i in range(0, len(parents) - 1, 2):
        p1 = parents[i]
        p2 = parents[i + 1]

        child1 = Individual(geneticAlgorithm.num_triangles, geneticAlgorithm.width, geneticAlgorithm.height)
        child2 = Individual(geneticAlgorithm.num_triangles, geneticAlgorithm.width, geneticAlgorithm.height)

        crossover_point1 = random.randint(1, geneticAlgorithm.num_triangles - 1)
        crossover_point2 = random.randint(crossover_point1, geneticAlgorithm.num_triangles - 1)

        if crossover_point1 > crossover_point2:
            crossover_point1, crossover_point2 = crossover_point2, crossover_point1

        child1.chromosome = copy.deepcopy(p1.chromosome[:crossover_point1]
                                        + p2.chromosome[crossover_point1:crossover_point2]
                                        + p1.chromosome[crossover_point2:])
        child2.chromosome = copy.deepcopy(p2.chromosome[:crossover_point1]
                                        + p1.chromosome[crossover_point1:crossover_point2]
                                        + p2.chromosome[crossover_point2:])

        children.extend([child1, child2])
    return children