#one_point.py
import random
import copy
from typing import List
from individual import Individual
from genetic_algorithm import GeneticAlgorithm

def crossover_one_point(ga: GeneticAlgorithm, parents: List[Individual]) -> List[Individual]:
    """Cruza una lista de padres por pares usando crossover de un solo punto."""
    children: List[Individual] = []

    # Emparejar padres de a dos
    for i in range(0, len(parents) - 1, 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]

        crossover_point = random.randint(1, ga.num_triangles - 1)

        child1 = Individual(ga.num_triangles, ga.width, ga.height)
        child2 = Individual(ga.num_triangles, ga.width, ga.height)

        child1.chromosome = copy.deepcopy(
            parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:]
        )
        child2.chromosome = copy.deepcopy(
            parent2.chromosome[:crossover_point] + parent1.chromosome[crossover_point:]
        )

        children.append(child1)
        children.append(child2)

    return children
