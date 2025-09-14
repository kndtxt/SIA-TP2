#one_point.py
import random
import copy
from typing import List
from individual import Individual
from genetic_algorithm import GeneticAlgorithm

def crossover_one_point(geneticAlgorithm: GeneticAlgorithm, parent1: Individual, parent2: Individual) -> List[Individual]:
        """Cruce de un solo punto."""
        child1 = Individual(geneticAlgorithm.num_triangles, geneticAlgorithm.width, geneticAlgorithm.height)
        child2 = Individual(geneticAlgorithm.num_triangles, geneticAlgorithm.width, geneticAlgorithm.height)
        
        crossover_point = random.randint(1, geneticAlgorithm.num_triangles - 1)
        
        child1.chromosome = copy.deepcopy(parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:])
        child2.chromosome = copy.deepcopy(parent2.chromosome[:crossover_point] + parent1.chromosome[crossover_point:])
        
        return [child1, child2]