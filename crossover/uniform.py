from individual import Individual
import random
import copy
from typing import List

def crossover_uniform(self, parent1: Individual, parent2: Individual) -> List[Individual]:
    """Cruce uniforme."""
    child1 = Individual(self.num_triangles, self.width, self.height)
    child2 = Individual(self.num_triangles, self.width, self.height)

    for i in range(self.num_triangles):
        if random.random() < 0.5:
            child1.chromosome[i] = copy.deepcopy(parent1.chromosome[i])
            child2.chromosome[i] = copy.deepcopy(parent2.chromosome[i])
        else:
            child1.chromosome[i] = copy.deepcopy(parent2.chromosome[i])
            child2.chromosome[i] = copy.deepcopy(parent1.chromosome[i])
    
    return [child1, child2]