# main.py
import os
from PIL import Image
from genetic_algorithm import GeneticAlgorithm
import json
from crossover.one_point import crossover_one_point
from crossover.uniform import crossover_uniform
from selection import boltzmann, elitist, ranking, roulette, tournament_deterministic, tournament_probabilistic, universal

# --- HIPERPARÁMETROS ---
TARGET_IMAGE_PATH = "images/input.png"  # La imagen que quieres replicar
OUTPUT_DIR = "images/output"            # Carpeta para guardar resultados

# Parámetros de la imagen
RESIZE_FACTOR = 1  # Reducir la imagen para que el proceso sea más rápido (ej. 0.25 = 1/4 del tamaño)

# Parámetros del Algoritmo Genético
POPULATION_SIZE = 50
K_SIZE = 25
NUM_TRIANGLES = 50
NUM_GENERATIONS = 1000
MUTATION_RATE = 0.8   # Probabilidad de que un nuevo individuo mute

#variaciones del algoritmo
SELECTION_METHOD = roulette.selection_roulette
CROSSOVER_METHOD = any


with open('./configs/run_config.json', 'r') as f:
    config = json.load(f)
    TARGET_IMAGE_PATH = config.get("TARGET_IMAGE_PATH", TARGET_IMAGE_PATH)
    OUTPUT_DIR = config.get("OUTPUT_DIR", OUTPUT_DIR)
    RESIZE_FACTOR = config.get("RESIZE_FACTOR", RESIZE_FACTOR)
    POPULATION_SIZE = config.get("POPULATION_SIZE", POPULATION_SIZE)
    NUM_TRIANGLES = config.get("NUM_TRIANGLES", NUM_TRIANGLES)
    NUM_GENERATIONS = config.get("NUM_GENERATIONS", NUM_GENERATIONS)
    MUTATION_RATE = config.get("MUTATION_RATE", MUTATION_RATE)
    SELECTION_METHOD = config.get("SELECTION_CONFIG", SELECTION_METHOD)
    if SELECTION_METHOD == "roulette":
        SELECTION_METHOD = roulette.selection_roulette
    else:
        raise ValueError(f"Método de selección desconocido: {SELECTION_METHOD}")

    CROSSOVER_METHOD = config.get("CROSSOVER_CONFIG", CROSSOVER_METHOD)
    if CROSSOVER_METHOD == "one_point":
        CROSSOVER_METHOD = crossover_one_point
    elif CROSSOVER_METHOD == "uniform":
        CROSSOVER_METHOD = crossover_uniform
    else:
        raise ValueError(f"Método de cruce desconocido: {CROSSOVER_METHOD}")

def main():
    print("Iniciando el compresor de imágenes con Algoritmos Genéticos...")

    # Crear directorio de salida si no existe
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. ============ Cargar y preparar la imagen objetivo ============
    print(f"Cargando imagen objetivo desde: {TARGET_IMAGE_PATH}")
    target_image = Image.open(TARGET_IMAGE_PATH).convert("RGB")
    
    original_size = target_image.size
    new_size = (int(original_size[0] * RESIZE_FACTOR), int(original_size[1] * RESIZE_FACTOR))
    
    print(f"Redimensionando imagen a {new_size} para un procesamiento más rápido.")
    target_image = target_image.resize(new_size)

    # 2. ============ Inicializar el Algoritmo Genético ============
    ga = GeneticAlgorithm(
        target_image=target_image,
        pop_size=POPULATION_SIZE,
        k=K_SIZE,
        num_triangles=NUM_TRIANGLES,
        mutation_rate=MUTATION_RATE
    )

    # 3. ============ Ciclo evolutivo ============
    print("\n--- Iniciando evolución ---")
    for i in range(NUM_GENERATIONS):
        print(f"\n--- Generación {i + 1}/{NUM_GENERATIONS} ---")
        ga.run_generation(selection_method=SELECTION_METHOD, crossover_method=CROSSOVER_METHOD)
        
        best_ind = ga.get_best_individual()
        
        # Imprimir métricas
        print(f"Mejor Fitness: {best_ind.fitness:.4f}")
        
        # Guardar imagen de progreso periódicamente
        if (i + 1) % 25 == 0:
            output_path = os.path.join(OUTPUT_DIR, f"generation_{i+1}.png")
            print(f"Guardando progreso en: {output_path}")
            best_ind.image.save(output_path)

    # 4. ============ Guardar el resultado final ============
    print("\n--- Evolución finalizada ---")
    final_best = ga.get_best_individual()
    final_output_path = os.path.join(OUTPUT_DIR, "final_result.png")
    
    print(f"Guardando la mejor imagen en: {final_output_path}")
    # Redimensionamos al tamaño original para una mejor visualización
    final_best.image.resize(original_size, Image.Resampling.LANCZOS).save(final_output_path)

    print("\n¡Proceso completado!")


if __name__ == "__main__":
    main()