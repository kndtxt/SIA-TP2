 
from individual import Individual
from triangle import Triangle
import random
import copy
from typing import List

def crossover_one_point(self, parent1: Individual, parent2: Individual) -> List[Individual]:
    """Cruce de un solo punto."""
    child1 = Individual(self.num_triangles, self.width, self.height)
    child2 = Individual(self.num_triangles, self.width, self.height)

    genes_per_triangle = 4  # 3 vertices (x, y) + color (r, g, b, a) = 4 genes por triangulo
    num_genes = self.num_triangles * genes_per_triangle
    
    crossover_point = random.randint(1, num_genes - 1)

    if crossover_point % genes_per_triangle == 0:
        a = crossover_point / genes_per_triangle
        ## copia por cromosomas
        child1.chromosome = copy.deepcopy(parent1.chromosome[:a] + parent2.chromosome[a:])
        child2.chromosome = copy.deepcopy(parent2.chromosome[:a] + parent1.chromosome[a:])
    else:
        a = crossover_point // genes_per_triangle
        b = a + 2
        c = crossover_point % genes_per_triangle
        ## copia por genes
        child1.chromosome = copy.deepcopy(parent1.chromosome[:a] + parent2.chromosome[b:])
        eve = Triangle(self.width, self.height)
        if c > 2:
            eve.points = parent1.chromosome[a+1].points
        else:
            for i in range(c):
                eve.points[i] = parent1.chromosome[a+1].points[i]
            for i in range(c, genes_per_triangle):
                eve.points[i] = parent2.chromosome[a+1].points[i]

        eve.color = parent2.chromosome[a+1].color
        child1.chromosome.append(eve)

        child2.chromosome = copy.deepcopy(parent2.chromosome[:a] + parent1.chromosome[b:])
        eve = Triangle(self.width, self.height)
        if c > 2:
            eve.points = parent2.chromosome[a+1].points
        else:
            for i in range(c):
                eve.points[i] = parent2.chromosome[a+1].points[i]
            for i in range(c, genes_per_triangle):
                eve.points[i] = parent1.chromosome[a+1].points[i]
                
        eve.color = parent1.chromosome[a+1].color
        child2.chromosome.append(eve)

    return [child1, child2]