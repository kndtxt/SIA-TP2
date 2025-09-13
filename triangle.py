# triangle.py
import random
from dataclasses import dataclass, field

# Un punto en 2D (x, y)
Point = tuple[int, int]

# Un color con transparencia (Rojo, Verde, Azul, Alfa)
Color = tuple[int, int, int, int]

@dataclass
class Triangle:
    """Representa un único triángulo con sus vértices y color."""
    points: list[Point] = field(default_factory=list)
    color: Color = (0, 0, 0, 0)

    @staticmethod
    def create_random(width: int, height: int) -> 'Triangle':
        """
        Crea un triángulo con coordenadas y color completamente aleatorios.
        El canal Alfa (transparencia) se mantiene bajo para que los colores se mezclen.
        """
        # Genera 3 puntos aleatorios dentro de los límites de la imagen
        points = [(random.randint(0, width), random.randint(0, height)) for _ in range(3)]
        
        # Genera un color aleatorio (R, G, B) y una transparencia (A)
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            100#random.randint(30, 255) # Se prefiere una transparencia media-baja
        )
        return Triangle(points, color)