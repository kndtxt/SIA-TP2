from individual import Individual
from triangle import Triangle
import random
import copy
from typing import List

def crossover_one_point(self, parent1: Individual, parent2: Individual) -> List[Individual]:
    """
    Cruce de un solo punto con posibilidad de cruzar *dentro* de un triángulo.
    genes_per_triangle = 4 (p0, p1, p2, color)
    """
    child1 = Individual(self.num_triangles, self.width, self.height)
    child2 = Individual(self.num_triangles, self.width, self.height)

    genes_per_triangle = 4  # chunk por triángulo: punto0, punto1, punto2, color
    num_genes = self.num_triangles * genes_per_triangle

    crossover_point = random.randint(1, num_genes - 1)

    triangle_idx = crossover_point // genes_per_triangle
    offset = crossover_point % genes_per_triangle

    if offset == 0:
        child1.chromosome = copy.deepcopy(parent1.chromosome[:triangle_idx] + parent2.chromosome[triangle_idx:])
        child2.chromosome = copy.deepcopy(parent2.chromosome[:triangle_idx] + parent1.chromosome[triangle_idx:])
        return [child1, child2]

    prefix1 = copy.deepcopy(parent1.chromosome[:triangle_idx])
    prefix2 = copy.deepcopy(parent2.chromosome[:triangle_idx])

    tri_a = parent1.chromosome[triangle_idx]
    tri_b = parent2.chromosome[triangle_idx]

    def make_mixed(tri_from_A: Triangle, tri_from_B: Triangle, off: int) -> Triangle:
        mixed = Triangle.create_random(self.width, self.height)
        pts = [None, None, None]
        for i in range(3):
            if i < off:
                pts[i] = tri_from_A.points[i]
            else:
                pts[i] = tri_from_B.points[i]
        mixed.points = pts

        mixed.color = tri_from_B.color
        return mixed

    mixed1 = make_mixed(tri_a, tri_b, offset)
    mixed2 = make_mixed(tri_b, tri_a, offset) 

    suffix_from_parent2 = copy.deepcopy(parent2.chromosome[triangle_idx+1:]) if (triangle_idx + 1) <= (len(parent2.chromosome)-1) else []
    suffix_from_parent1 = copy.deepcopy(parent1.chromosome[triangle_idx+1:]) if (triangle_idx + 1) <= (len(parent1.chromosome)-1) else []


    child1.chromosome = prefix1 + [mixed1] + suffix_from_parent2
    child2.chromosome = prefix2 + [mixed2] + suffix_from_parent1

    def pad_to_length(chrom, target_len, template_parent):
        while len(chrom) < target_len:
            chrom.append(copy.deepcopy(template_parent.chromosome[-1]))
        if len(chrom) > target_len:
            chrom = chrom[:target_len]
        return chrom

    target_len = self.num_triangles
    child1.chromosome = pad_to_length(child1.chromosome, target_len, parent1)
    child2.chromosome = pad_to_length(child2.chromosome, target_len, parent2)

    return [child1, child2]
