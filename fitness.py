# fitness.py
import numpy as np
from PIL import Image

def calculate_fitness(generated_image: Image.Image, target_image: Image.Image) -> float:
    """
    Calcula la aptitud de una imagen generada comparándola con la imagen objetivo.
    La aptitud es inversamente proporcional al error cuadrático medio.

    Args:
        generated_image: La imagen creada a partir de los triángulos.
        target_image: La imagen que se intenta replicar.

    Returns:
        Un valor de punto flotante que representa la aptitud (más alto es mejor).
    """
    # Convierte las imágenes a arrays de NumPy para cálculos rápidos
    target_arr = np.array(target_image, dtype=np.int64)
    generated_arr = np.array(generated_image, dtype=np.int64)

    # Calcula la suma de las diferencias al cuadrado
    # Es la base del Error Cuadrático Medio (MSE)
    error = np.sum((target_arr - generated_arr) ** 2)

    fitness = 1.0 / (1.0 + error)
    
    return fitness