import random
import copy
from typing import List, Tuple
from individual import Individual
from triangle import Triangle

Point = Tuple[int, int]

def crossover_uniform(self, parent1: Individual, parent2: Individual) -> List[Individual]:
    """
    Cruce uniforme a nivel de atributos dentro de cada triángulo.
    Para cada triángulo i y para cada atributo (p0,p1,p2,color):
      - child1 recibe el atributo de parent1 con prob 0.5, si no lo recibe de parent2
      - child2 recibe el atributo complementario (si child1 tomó de parent1, child2 toma de parent2)
    Esto evita aliasing y deja la longitud de cromosoma exactamente = num_triangles.
    """
    child1 = Individual(self.num_triangles, self.width, self.height)
    child2 = Individual(self.num_triangles, self.width, self.height)
    child1.chromosome = []
    child2.chromosome = []


    for i in range(self.num_triangles):
        tri_a = parent1.chromosome[i]
        tri_b = parent2.chromosome[i]

        new_pts_1 = [None, None, None]
        new_pts_2 = [None, None, None]

        # Para cada punto (3 puntos)
        for p_idx in range(3):
            if random.random() > 0.5:
                new_pts_1[p_idx] = copy.deepcopy(tri_a.points[p_idx])
                new_pts_2[p_idx] = copy.deepcopy(tri_b.points[p_idx])
            else:
                new_pts_1[p_idx] = copy.deepcopy(tri_b.points[p_idx])
                new_pts_2[p_idx] = copy.deepcopy(tri_a.points[p_idx])

        # Para el color: tratamos la tupla RGBA como unidad
        if random.random() > 0.5:
            new_color_1 = copy.deepcopy(tri_a.color)
            new_color_2 = copy.deepcopy(tri_b.color)
        else:
            new_color_1 = copy.deepcopy(tri_b.color)
            new_color_2 = copy.deepcopy(tri_a.color)

        # Crear Triangles concretos (asegurarse de respetar la forma del dataclass)
        t1 = Triangle(points=new_pts_1, color=new_color_1)
        t2 = Triangle(points=new_pts_2, color=new_color_2)

        child1.chromosome.append(t1)
        child2.chromosome.append(t2)

    # Seguridad: asegurarse de que la longitud es correcta
    child1.chromosome = child1.chromosome[: self.num_triangles]
    child2.chromosome = child2.chromosome[: self.num_triangles]

    return [child1, child2]
