# main.py
import os
import json
import sys
from time import time
from tqdm import tqdm
from PIL import Image
from genetic_algorithm import GeneticAlgorithm
from selection import boltzmann, elitist, ranking, roulette, tournament_deterministic, tournament_probabilistic, universal
from crossovers import anular, one_point, two_point, uniform, one_point_fake
from mutations import mutation_methods
from write_to_file import delete_existing_file, write_to_file

epsilon = 1e-6

sel_meth = ["roulette", "ranking", "tournament_deterministic", 
            "tournament_probabilistic", "universal", "elitist", 
            "boltzmann"]
cross_meth = ["anular", "one_point", "two_point", "uniform", "one_point_fake"]
mut_meth = ["basic", "uniform", "limited", "complete"]
rep_strat = ["traditional", "generational", "steady_state"]


#change config based on args
def update_config():
    with open('./configs/config.json') as f:
        config = json.load(f)
    if len(sys.argv) > 2:
        config["pop_size"] = int(sys.argv[2])
    if len(sys.argv) > 3:
        config["k"] = int(sys.argv[3])
    if len(sys.argv) > 4:
        config["num_triangles"] = int(sys.argv[4])
    if len(sys.argv) > 5:
        config["num_generations"] = int(sys.argv[5])
    if len(sys.argv) > 6:
        config["selection_method"] = sys.argv[6]
    if len(sys.argv) > 6:
        config["generation_selection_method"] = sys.argv[6]
    if len(sys.argv) > 7:
        config["generation_selection_method"] = sys.argv[7]
    if len(sys.argv) > 8:
        config["crossover_method"] = sys.argv[8]
    if len(sys.argv) > 9:
        config["mutation_method"] = sys.argv[9]
    if len(sys.argv) > 10:
        config["replacement_strategy"] = sys.argv[10]
    with open('./configs/config.json', 'w') as f:
        json.dump(config, f, indent=4)


# Cargar configuración desde JSON
def load_config(path="./configs/config.json"):
    with open(path, "r") as file:
        return json.load(file)
    
SELECTION_METHODS = {
    "boltzmann": boltzmann.selection_boltzmann,
    "elitist": elitist.selection_elitist,
    "ranking": ranking.selection_ranking,
    "roulette": roulette.selection_roulette,
    "tournament_deterministic": tournament_deterministic.selection_tournament_deterministic,
    "tournament_probabilistic": tournament_probabilistic.selection_tournament_probabilistic,
    "universal": universal.selection_universal
}

CROSSOVER_METHODS = {
    "anular": anular.crossover_anular,
    "one_point": one_point.crossover_one_point,
    "two_point": two_point.crossover_two_point,
    "uniform": uniform.crossover_uniform,
    "one_point_fake": one_point_fake.crossover_one_point
}

MUTATION_METHODS = {
    "basic": mutation_methods.basic_mutation,
    "uniform": mutation_methods.multigen_uniform_mutation,
    "limited": mutation_methods.multigen_limited_mutation,
    "complete": mutation_methods.complete_mutation
}

best_fitness_threshold = {
    "threshold": 0.05,
    "no_improvement_limit": 100,
    "tally": 0
}

def main():
    update_config()
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
    # name_method = sys.argv[1] if len(sys.argv) > 1 else "default"
    name_method = f'{config["selection_method"]}_{config["crossover_method"]}_{config["mutation_method"]}_{config["replacement_strategy"]}_k{config["k"]}_pop{config["pop_size"]}_gen{config["num_generations"]}'

    selection_fn = SELECTION_METHODS.get(config["selection_method"])
    generation_selection_fn = SELECTION_METHODS.get(config["generation_selection_method"])
    crossover_fn = CROSSOVER_METHODS.get(config["crossover_method"])
    mutation_fn = MUTATION_METHODS.get(config["mutation_method"])
    replacement_strategy = (config["replacement_strategy"])

    # Condiciones de corte
    #gets fitness threshold from config if exists -> else default value
    best_fitness_threshold["threshold"] = config.get("FITNESS_THRESHOLD", best_fitness_threshold["threshold"])
    prev_best_fitness = -1.0

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
        k=K_SIZE,
        num_triangles=NUM_TRIANGLES,
        mutation_rate=MUTATION_RATE
    )

    delete_existing_file(f"fitness_log_{name_method}.txt")
    delete_existing_file(f"time_log_{name_method}.txt")
    write_to_file(f"fitness_log_{name_method}.txt", "Generación;Mejor Fitness\n")
    start_time = time()
    write_to_file(f"time_log_{name_method}.txt", f"Tiempo inicial: {start_time}\n")
    # Ciclo evolutivo
    print("\n--- Iniciando evolución ---")
    for i in tqdm(range(NUM_GENERATIONS), desc="Evolucionando"):
        print(f"\n--- Generación {i + 1}/{NUM_GENERATIONS} ---")
        if(config["selection_method"] == "boltzmann"):

            #boltzmann necesita la generacion actual para el calculo de temperatura
            ga.run_generation(selection=selection_fn, crossover=crossover_fn, mutation=mutation_fn, 
                              replacement_strategy=replacement_strategy, generation_selection=generation_selection_fn, generation=i)
        else:
            ga.run_generation(selection=selection_fn, crossover=crossover_fn, mutation=mutation_fn, 
                              replacement_strategy=replacement_strategy, generation_selection=generation_selection_fn)

        best_ind = ga.get_best_individual()
        
        # Imprimir métricas
        print(f"Mejor Fitness: {best_ind.fitness:.10f}")
        
        # Guardar imagen de progreso periódicamente
        if (i + 1) % 25 == 0:
            output_path = os.path.join(OUTPUT_DIR + name_method, f"generation_{name_method}_{i+1}.png")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            print(f"Guardando progreso en: {output_path}")
            best_ind.image.save(output_path)

        # Impresion a archivo
        write_to_file(f"fitness_log_{name_method}.txt", f"{i + 1};{best_ind.fitness:.10f}\n")

        if best_fitness_threshold["threshold"] <= best_ind.fitness:
            print(f"Condición de parada alcanzada: Fitness >= {best_fitness_threshold['threshold']}.")
            break
        else:
            if abs(prev_best_fitness - best_ind.fitness) < epsilon:
                best_fitness_threshold["tally"] += 1
            else:
                best_fitness_threshold["tally"] = 0
            prev_best_fitness = best_ind.fitness
            if best_fitness_threshold["tally"] >= best_fitness_threshold["no_improvement_limit"]:
                print(f"Condición de parada alcanzada: El mejor fitness no ha mejorado en {best_fitness_threshold['no_improvement_limit']} generaciones.")
                break

    # Guardar el resultado final
    print("\n--- Evolución finalizada ---")
    end_time = time()
    write_to_file(f"time_log_{name_method}.txt", f"Tiempo final: {end_time}\n")
    write_to_file(f"time_log_{name_method}.txt", f"Tiempo total de ejecución (segundos): {end_time - start_time}\n")
    final_best = ga.get_best_individual()
    final_output_path = os.path.join(OUTPUT_DIR, f"final_result_name_method.png")
    os.makedirs(os.path.dirname(final_output_path), exist_ok=True)
    print(f"Guardando la mejor imagen en: {final_output_path}")
    final_best.image.save(final_output_path)

    print("\n¡Proceso completado!")
    

if __name__ == "__main__":
    main()