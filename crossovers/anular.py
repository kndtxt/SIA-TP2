# anular.py

from individual import Individual
import random
import copy
from typing import List
from genetic_algorithm import GeneticAlgorithm

def crossover_anular(geneticAlgorithm: GeneticAlgorithm, parents:List[Individual]) -> List[Individual]:
    """Cruce de un solo punto."""
    children = []

    for i in range(0, len(parents) - 1, 2):
        p1 = parents[i]
        p2 = parents[i + 1]

        child1 = Individual(geneticAlgorithm.num_triangles, geneticAlgorithm.width, geneticAlgorithm.height)
        child2 = Individual(geneticAlgorithm.num_triangles, geneticAlgorithm.width, geneticAlgorithm.height)
        
        crossover_point = random.randint(1, segeneticAlgorithmlf.num_triangles - 1)
        
        child1.chromosome = copy.deepcopy(p1.chromosome[:crossover_point] + p2.chromosome[crossover_point:])
        child2.chromosome = copy.deepcopy(p2.chromosome[:crossover_point] + p1.chromosome[crossover_point:])
        
        # [[11111][11231][12331][123131]],[[11111][11231][12331][123131]],[[11111][11231][12331][123131]]
        #     1         2         3         4         5

        children.extend([child1, child2])
    return children