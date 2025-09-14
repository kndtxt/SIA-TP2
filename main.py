# main.py
import os
import json
from tqdm import tqdm
from PIL import Image
from genetic_algorithm import GeneticAlgorithm
from selection import roulette, tournament_deterministic
from crossovers import one_point

# Cargar configuración desde JSON
def load_config(path="./configs/config.json"):
    with open(path, "r") as file:
        return json.load(file)
    
SELECTION_METHODS = {
    "roulette": roulette.selection_roulette,
    "tournament_deterministic": tournament_deterministic.selection_tournament,
}

CROSSOVER_METHODS = {
    "one_point": one_point.crossover_one_point,
}

MUTATION_METHODS = {

}

def main():
    print("Iniciando el compresor de imágenes con Algoritmos Genéticos...")

    # Cargar data de config
    config = load_config()
    OUTPUT_DIR = (config["output_dir"])
    TARGET_IMAGE_PATH = (config["target_image_path"])

    POPULATION_SIZE = (config["pop_size"])
    NUM_TRIANGLES = (config["num_triangles"])
    NUM_GENERATIONS = (config["num_generations"])
    MUTATION_RATE = (config["mutation_rate"])
    K_SIZE = (config["k"])

    selection_fn = SELECTION_METHODS.get(config["selection_method"])
    crossover_fn = CROSSOVER_METHODS.get(config["crossover_method"])
    #mutation_fn = MUTATION_METHODS.get(config["mutation_method"])
    replacement_strategy = (config["replacement_strategy"])

    # Crear directorio de salida si no existe
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Cargar y preparar la imagen objetivo
    print(f"Cargando imagen objetivo desde: {TARGET_IMAGE_PATH}")
    target_image = Image.open(TARGET_IMAGE_PATH).convert("RGB")

    # Inicializar el Algoritmo Genético
    ga = GeneticAlgorithm(
        target_image=target_image,
        pop_size=POPULATION_SIZE,
        num_triangles=NUM_TRIANGLES,
        mutation_rate=MUTATION_RATE
    )

    # Ciclo evolutivo
    print("\n--- Iniciando evolución ---")
    for i in tqdm(range(NUM_GENERATIONS), desc="Evolucionando"):
        print(f"\n--- Generación {i + 1}/{NUM_GENERATIONS} ---")
        ga.run_generation(selection_fn, crossover_fn)
        
        best_ind = ga.get_best_individual()
        
        # Imprimir métricas
        print(f"Mejor Fitness: {best_ind.fitness:.10f}")
        
        # Guardar imagen de progreso periódicamente
        if (i + 1) % 25 == 0:
            output_path = os.path.join(OUTPUT_DIR, f"generation_{i+1}.png")
            print(f"Guardando progreso en: {output_path}")
            best_ind.image.save(output_path)

    # Guardar el resultado final
    print("\n--- Evolución finalizada ---")
    final_best = ga.get_best_individual()
    final_output_path = os.path.join(OUTPUT_DIR, "final_result.png")
    
    print(f"Guardando la mejor imagen en: {final_output_path}")
    final_best.image.save(final_output_path)

    print("\n¡Proceso completado!")


if __name__ == "__main__":
    main()