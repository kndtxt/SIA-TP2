# fitness.py
import numpy as np
from PIL import Image

# def calculate_fitness(generated_image: Image.Image, target_image: Image.Image) -> float:

#     # Convierte las imágenes a arrays de NumPy para cálculos rápidos
#     target_arr = np.array(target_image, dtype=np.int64)
#     generated_arr = np.array(generated_image, dtype=np.int64)

#     # Calcula la suma de las diferencias al cuadrado
#     # Es la base del Error Cuadrático Medio (MSE)
#     error = np.sum((target_arr - generated_arr) ** 2)

#     # Normaliza el error para que sea más manejable
#     # Se divide por el máximo error posible
#     max_error = target_arr.size * (255 ** 2)
#     normalized_error = error / max_error

#     # La aptitud es 1.0 para un error de 0 y tiende a 0 para errores grandes.
#     #fitness = 1.0 - normalized_error
#     fitness = 1.0 / (1.0 + error)
    
#     return fitness

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
    target_arr = np.array(target_image, dtype=np.int64)
    generated_arr = np.array(generated_image, dtype=np.int64)
    error = np.sum((target_arr - generated_arr) ** 2)
    max_error = target_arr.size * (255 ** 2)
    normalized_error = error / max_error  # ∈ [0, 1]
    # Opción A (intuitiva): 1 - error normalizado
    # fitness = 1.0 - normalized_error  # ∈ [0,1], 1 es perfecto
    # Opción B (suave, evita 0 exacto): 1 / (1 + error normalizado)
    fitness = 1.0 / (1.0 + normalized_error)  # ∈ (0,1], 1 es perfecto
    return float(fitness)
