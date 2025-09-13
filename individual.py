# individual.py
import random
from typing import List
from PIL import Image
from triangle import Triangle
from renderer import render
from fitness import calculate_combined_fitness, calculate_ssim_fitness, calculate_mse_fitness

class Individual:
    """
    Representa una solución candidata: una colección de triángulos.
    """

    def __init__(self, num_triangles: int, img_width: int, img_height: int):
        self.img_width = img_width
        self.img_height = img_height
        # El "cromosoma" es la lista de genes (triángulos)
        self.chromosome: List[Triangle] = [
            Triangle.create_random(img_width, img_height) for _ in range(num_triangles)
        ]
        self.fitness = -1.0
        self.relative_fitness = -1.0
        self.pseudo_fitness = -1.0
        self.relative_pseudo_fitness = -1.0
        self._image: Image.Image = None

    @property
    def image(self) -> Image.Image:
        """Renderiza la imagen si no ha sido creada todavía."""
        if self._image is None:
            self._image = render(self.chromosome, self.img_width, self.img_height)
        return self._image

    def calculate_fitness(self, target_image: Image.Image):
        """Calcula y almacena la aptitud del individuo."""
        self.fitness = calculate_ssim_fitness(self.image, target_image)

    def calculate_relative_fitness(self, total_fitness):
        """Calcula y almacena la aptitud del relativa individuo."""
        self.relative_fitness = self.fitness / total_fitness

    # Mutation in our nation   -b(￣▽￣)d-
    # ༼ つ ◕_◕ ༽つ


    def mutate_gene(self, mutation_rate):
        """
        Se altera un solo gen (triángulo) aleatorio.
        """
        if random.random() < mutation_rate:
            self._mutate_one_gene()
            self._image = None

    """  def mutate_multigen_limited(self, m: int):
        
        Se selecciona un número aleatorio de genes en [1, M] y se mutan.
        
        num_to_mutate = random.randint(1, m)
        for _ in range(num_to_mutate):
            if random.random() < MUTATION_RATE:
                self._mutate_one_gene()

        self._image = None
    """

    def mutate_multigen_uniform(self, mutation_rate):
        """
        Recorro todos los genes, SI SON 4 GENES, NO SON 10 CARACTERISTICAS
        (coordenadas y color de cada triángulo).
        Cada uno tiene probabilidad MUTATION_RATE de mutar.
        """
        for tri in self.chromosome:

            if random.random() < mutation_rate:
                tri.points[0] = (
                    random.randint(0, self.img_width),
                    random.randint(0, self.img_height)
                )

            if random.random() < mutation_rate:
                tri.points[1] = (
                    random.randint(0, self.img_width),
                    random.randint(0, self.img_height)
                )

            if random.random() < mutation_rate:
                tri.points[2] = (
                    random.randint(0, self.img_width),
                    random.randint(0, self.img_height)
                )

            if random.random() < mutation_rate:
                tri.color = (
                    random.randint(0, 255),  # R
                    random.randint(0, 255),  # G
                    random.randint(0, 255),  # B
                    random.randint(30, 100)   # A
                )

        # Invalido la caché de la imagen
        self._image = None


    def mutate_complete(self, mutation_rate):
        
        """Mutación Completa: Todos los genes se mutan."""
        for tri in self.chromosome:
            if random.random() < mutation_rate:
                tri.points[0] = (
                    random.randint(0, self.img_width),
                    random.randint(0, self.img_height)
                )

                tri.points[1] = (
                    random.randint(0, self.img_width),
                    random.randint(0, self.img_height)
                )

                tri.points[2] = (
                    random.randint(0, self.img_width),
                    random.randint(0, self.img_height)
                )

                tri.color = (
                    random.randint(0, 255),  # R
                    random.randint(0, 255),  # G
                    random.randint(0, 255),  # B
                    random.randint(30, 100)  # A
                )

        self._image = None


    def _mutate_one_gene(self):
        """Elige un triángulo al azar y lo muta."""
        tri_to_mutate = random.choice(self.chromosome)
        self.mutate_one_specific_gene(tri_to_mutate)

    def mutate_one_specific_gene(self, tri_to_mutate: Triangle):
        """
        Aplica una pequeña mutación a un gen (triángulo) aleatorio.
        Cambia un solo valor (una coordenada o un canal de color).
        """
        # Elige si mutar un punto o el color
        if random.random() < 0.5: # Mutar un punto
            point_idx = random.randint(0, 2)
            coord_idx = random.randint(0, 1) # 0 para x, 1 para y
            new_val = random.randint(0, self.img_width if coord_idx == 0 else self.img_height)
            points_list = list(tri_to_mutate.points)
            point_to_change = list(points_list[point_idx])
            point_to_change[coord_idx] = new_val
            points_list[point_idx] = tuple(point_to_change)
            tri_to_mutate.points = points_list
        else: # Mutar el color
            color_idx = random.randint(0, 3)
            new_val = random.randint(0 if color_idx < 3 else 30, 255 if color_idx < 3 else 100)
            new_color = list(tri_to_mutate.color)
            new_color[color_idx] = new_val
            tri_to_mutate.color = tuple(new_color)

