
import copy
from individual import Individual
import random
from typing import List





class Crossover:
    def __init__(self):
        pass

    def _crossover_one_point(self, parent1: Individual, parent2: Individual, width: int, height: int, num_triangles: int) -> List[Individual]:
        """Cruce de un solo punto."""
        child1 = Individual(num_triangles, width, height)
        child2 = Individual(num_triangles, width, height)

        crossover_point = random.randint(1, num_triangles - 1)

        
        child1.chromosome = copy.deepcopy(parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:])
        child2.chromosome = copy.deepcopy(parent2.chromosome[:crossover_point] + parent1.chromosome[crossover_point:])
        
        return [child1, child2]

    def _crossover_uniform(self, parent1: Individual, parent2: Individual, width: int, height: int, num_triangles: int) -> List[Individual]:
        """Cruce uniforme."""
        child1 = Individual(num_triangles, width, height)
        child2 = Individual(num_triangles, width, height)

        for i in range(num_triangles):
            if random.random() < 0.5:
                child1.chromosome[i] = copy.deepcopy(parent1.chromosome[i])
                child2.chromosome[i] = copy.deepcopy(parent2.chromosome[i])
            else:
                child1.chromosome[i] = copy.deepcopy(parent2.chromosome[i])
                child2.chromosome[i] = copy.deepcopy(parent1.chromosome[i])
        
        return [child1, child2]
#        
#    def crossover_two_point(self, other, rng) -> tuple["Individual","Individual"]:
#        n = len(self.triangles)
#        i = rng.randrange(0, n-1)
#        j = rng.randrange(i+1, n)
#        t1 = self.triangles[:i] + other.triangles[i:j] + self.triangles[j:]
#        t2 = other.triangles[:i] + self.triangles[i:j] + other.triangles[j:]
#        return Individual([tri.clone() for tri in t1]), Individual([tri.clone() for tri in t2])
#