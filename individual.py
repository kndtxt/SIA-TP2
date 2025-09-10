# individual.py
import random
from typing import List
from PIL import Image
from triangle import Triangle
from renderer import render
from fitness import calculate_fitness
import logging
import logging.config
import json

def setup_logging(config_path="config/logger.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    logging.config.dictConfig(config)

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
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.fitness = -1.0
        self.relative_fitness = -1.0
        self.pseudo_fitness = -1.0
        self.relative_pseudo_fitness = -1.0 # por ahora no se usa
        self._image: Image.Image = None

    @property
    def image(self) -> Image.Image:
        """Renderiza la imagen si no ha sido creada todavía."""
        if self._image is None:
            self._image = render(self.chromosome, self.img_width, self.img_height)
        return self._image
    
    def calculate_fitness(self, target_image: Image.Image):
        """Calcula y almacena la aptitud del individuo."""
        self.fitness = calculate_fitness(self.image, target_image)
        self.logger.debug(f"Fitness calculado: {self.fitness}")


    def calculate_relative_fitness(self, max_fitness):
        """Calcula y almacena la aptitud del relativa individuo."""
        self.relative_fitness = self.fitness/max_fitness
        self.logger.debug(f"Relative Fitness calculado: {self.relative_fitness}")
    
    def mutate_gene(self):
        """
        Aplica una pequeña mutación a un gen (triángulo) aleatorio.
        Cambia un solo valor (una coordenada o un canal de color).
        """
        # Elige un triángulo al azar
        tri_to_mutate = random.choice(self.chromosome)
        
        # Elige si mutar un punto o el color
        if random.random() < 0.5: # Mutar un punto
            point_idx = random.randint(0, 2)
            coord_idx = random.randint(0, 1) # 0 para x, 1 para y
            
            new_val = random.randint(0, self.img_width if coord_idx == 0 else self.img_height)
            
            # Reconstruye el punto con el nuevo valor
            points_list = list(tri_to_mutate.points)
            point_to_change = list(points_list[point_idx])
            point_to_change[coord_idx] = new_val
            points_list[point_idx] = tuple(point_to_change)
            tri_to_mutate.points = points_list
        else: # Mutar el color
            color_idx = random.randint(0, 3)
            new_val = random.randint(0, 255 if color_idx < 3 else 100)
            
            new_color = list(tri_to_mutate.color)
            new_color[color_idx] = new_val
            tri_to_mutate.color = tuple(new_color)

        # La mutación cambió la imagen, así que debemos borrar la caché
        self._image = None