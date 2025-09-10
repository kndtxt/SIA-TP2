# main.py
import os
import sys
from PIL import Image
import json
import time
from genetic_algorithm import GeneticAlgorithm
import logging
import logging.config

# --- HIPERPARÁMETROS ---
TARGET_IMAGE_PATH = "images/"  # La imagen que quieres replicar
OUTPUT_DIR = "images/output"            # Carpeta para guardar resultados

# Parámetros de la imagen
RESIZE_FACTOR = 1  # Reducir la imagen para que el proceso sea más rápido (ej. 0.25 = 1/4 del tamaño)

# Parámetros del Algoritmo Genético
# POPULATION_SIZE = 250
# NUM_TRIANGLES = 50
# NUM_GENERATIONS = 5000
# ELITISM_COUNT = 25     # Cuántos de los mejores individuos sobreviven automáticamente
# MUTATION_RATE = 0.8   # Probabilidad de que un nuevo individuo mute

logger = logging.getLogger(__name__)

def setup_logging(config_path="config/logger.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    # Eliminar el archivo de log viejo si existe
    filename = config["handlers"]["file"]["filename"]
    if os.path.exists(filename):
        os.remove(filename)
    logging.config.dictConfig(config)

def read_config(config_path: str):

    with open(config_path, 'r') as f:
        config = json.load(f)
    
    crossover_type = config["crossover_type"]
    mutation_rate = config["mutation_rate"]
    population_size = config["population_size"]
    num_generations = config["steps"]
    num_triangles = config["triangles"]
    elitism_count = config["elitism_count"]
    image = config["image"]

    return population_size, num_triangles, num_generations, mutation_rate, image, crossover_type, elitism_count

def main(args=None):
    print("Iniciando el compresor de imágenes con Algoritmos Genéticos...")
    print(f"Usando {os.cpu_count()} hilos para procesamiento paralelo.\n")

    

    setup_logging()

    if args is None:
        print("Usa: python main.py <ruta_al_config.json>")
        return

    population_size, num_triangles, num_generations, mutation_rate, image, crossover_type, elitism_count = read_config(args[1])

    print(f"Parámetros:\n- Tamaño Población: {population_size}\n- Triángulos por Individuo: {num_triangles}\n- Generaciones: {num_generations}\n- Mutación: {mutation_rate*100}%\n- Elitismo: {elitism_count} individuos\n")

    # Crear directorio de salida si no existe
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Cargar y preparar la imagen objetivo
    print(f"Cargando imagen objetivo desde: {TARGET_IMAGE_PATH}")
    target_image = Image.open(TARGET_IMAGE_PATH + image).convert("RGB")

    original_size = target_image.size
    new_size = (int(original_size[0] * RESIZE_FACTOR), int(original_size[1] * RESIZE_FACTOR))
    
    print(f"Redimensionando imagen a {new_size} para un procesamiento más rápido.")
    target_image = target_image.resize(new_size)

    # 2. Inicializar el Algoritmo Genético
    ga = GeneticAlgorithm(
        target_image=target_image,
        pop_size=population_size,
        num_triangles=num_triangles,
        elitism_count=elitism_count,
        mutation_rate=mutation_rate
    )

    # 3. Ciclo evolutivo
    print("\n--- Iniciando evolución ---")
    start_time = time.time()
    for i in range(num_generations):
        print(f"\n--- Generación {i + 1}/{num_generations} ---")
        ga.run_generation()
        
        best_ind = ga.get_best_individual()
        
        # Imprimir métricas
        print(f"Mejor Fitness: {best_ind.fitness:.4f}")
        
        # Guardar imagen de progreso periódicamente
        if (i + 1) % 25 == 0:
            output_path = os.path.join(OUTPUT_DIR, f"generation_{i+1}.png")
            print(f"Guardando progreso en: {output_path}")
            best_ind.image.save(output_path)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTiempo total de evolución: {elapsed_time/60:.2f} minutos")

    # 4. Guardar el resultado final
    print("\n--- Evolución finalizada ---")
    final_best = ga.get_best_individual()
    final_output_path = os.path.join(OUTPUT_DIR, "final_result.png")
    
    print(f"Guardando la mejor imagen en: {final_output_path}")
    # Redimensionamos al tamaño original para una mejor visualización
    final_best.image.resize(original_size, Image.Resampling.LANCZOS).save(final_output_path)

    print("\n¡Proceso completado!")


if __name__ == "__main__":
    main(args=sys.argv)