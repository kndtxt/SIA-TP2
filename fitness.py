# fitness.py
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim

def calculate_mse_fitness(generated_image: Image.Image, target_image: Image.Image) -> float:
    """
    Fitness basado en el error cuadrático medio (MSE).
    """
    target_arr = np.array(target_image, dtype=np.float32)
    generated_arr = np.array(generated_image, dtype=np.float32)

    error = np.sum((target_arr - generated_arr) ** 2)
    max_error = target_arr.size * (255 ** 2)
    normalized_error = error / max_error

    return 1.0 - normalized_error


def calculate_ssim_fitness(generated_image: Image.Image, target_image: Image.Image) -> float:
    """
    Fitness basado en SSIM (Structural Similarity Index).
    """
    target_arr = np.array(target_image, dtype=np.uint8)
    generated_arr = np.array(generated_image, dtype=np.uint8)

    # SSIM trabaja por canal o en escala de grises, mejor promediar RGB
    ssim_value = 0.0
    for i in range(3):  # R, G, B
        ssim_value += ssim(target_arr[..., i], generated_arr[..., i], data_range=255)
    ssim_value /= 3.0

    return ssim_value


def calculate_combined_fitness(generated_image: Image.Image, target_image: Image.Image, alpha: float = 0.7) -> float:
    """
    Combina MSE y SSIM en una sola métrica.
    alpha controla la importancia relativa:
      - alpha=0.5 => igual peso para ambos
      - alpha>0.5 => da más peso al SSIM
    """
    mse_f = calculate_mse_fitness(generated_image, target_image)
    ssim_f = calculate_ssim_fitness(generated_image, target_image)

    return alpha * ssim_f + (1 - alpha) * mse_f
