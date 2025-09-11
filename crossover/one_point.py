 
from individual import Individual
import random
import copy
from typing import List

def crossover_one_point(self, parent1: Individual, parent2: Individual) -> List[Individual]:
    """Cruce de un solo punto."""
    child1 = Individual(self.num_triangles, self.width, self.height)
    child2 = Individual(self.num_triangles, self.width, self.height)
    
    crossover_point = random.randint(1, self.num_triangles - 1)
    
    child1.chromosome = copy.deepcopy(parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:])
    child2.chromosome = copy.deepcopy(parent2.chromosome[:crossover_point] + parent1.chromosome[crossover_point:])
    
    return [child1, child2]