from individual import Individual
import random
import copy
from typing import List
from triangle import Point, Triangle

genes_per_triangle = 4

def crossover_uniform(self, parent1: Individual, parent2: Individual) -> List[Individual]:
    """Cruce uniforme."""
    child1 = Individual(self.num_triangles, self.width, self.height)
    child2 = Individual(self.num_triangles, self.width, self.height)

    for i in range(self.num_triangles):

        triang1 = Triangle(self.width, self.height)
        triang2 = Triangle(self.width, self.height)

        rand = [] # genero 4 numeros random
        for j in range(genes_per_triangle):
            rand.append(random.random())

        triang1.points[0] = parent1.chromosome[i].points[0] if rand[0] > 0.5 else parent2.chromosome[i].points[0]
        triang1.points[1] = parent1.chromosome[i].points[1] if rand[1] > 0.5 else parent2.chromosome[i].points[1]
        triang1.points[2] = parent1.chromosome[i].points[2] if rand[2] > 0.5 else parent2.chromosome[i].points[2]
        triang1.color = parent1.chromosome[i].color if rand[3] > 0.5 else parent2.chromosome[i].color

        triang2.points[0] = parent1.chromosome[i].points[0] if rand[0] < 0.5 else parent2.chromosome[i].points[0]
        triang2.points[1] = parent1.chromosome[i].points[1] if rand[1] < 0.5 else parent2.chromosome[i].points[1]
        triang2.points[2] = parent1.chromosome[i].points[2] if rand[2] < 0.5 else parent2.chromosome[i].points[2]
        triang2.color = parent1.chromosome[i].color if rand[3] < 0.5 else parent2.chromosome[i].color

        child1.chromosome.append(triang1)
        child2.chromosome.append(triang2)

    return [child1, child2]