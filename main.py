# main.py
import os
import json
from PIL import Image
from tqdm import tqdm # Para la barra de progreso
from genetic_algorithm import GeneticAlgorithm
from selection import boltzmann, elitist, ranking, roulette, tournament_deterministic, tournament_probabilistic
from crossover import anular, one_point, two_point, uniform
from mutation_methods import basic_mutation, multigen_uniform_mutation, complete_mutation

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
}

CROSSOVER_METHODS = {
    "anular": anular.crossover_anular,
    "one_point": one_point.crossover_one_point,
    "two_point": two_point.crossover_two_point,
    "uniform": uniform.crossover_uniform,
}

MUTATION_METHODS = {
    "basic": basic_mutation,
    "uniform": multigen_uniform_mutation,
    "complete": complete_mutation
}

best_fitness_threshold = {
    "threshold": 0.95,
    "no_improvement_limit": 500,
    "tally": 0
}

def main():
    config = load_config()

    # Condiciones de corte
    best_fitness_threshold["threshold"] = config.get("FITNESS_THRESHOLD", best_fitness_threshold["threshold"])
    prev_best_fitness = -1.0

    output_dir = (config["output_dir"])

    # Crear directorio de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Cargar imagen objetivo
    target_image = Image.open(config["target_image_path"]).convert("RGB")

    # Crear el algoritmo genético
    ga = GeneticAlgorithm(
        target_image=target_image,
        pop_size=config["pop_size"],
        k=config["k"],
        num_triangles=config["num_triangles"],
        mutation_rate=config["mutation_rate"]
    )

    # Obtener funciones de selección y crossover
    selection_fn = SELECTION_METHODS.get(config["selection_method"])
    crossover_fn = CROSSOVER_METHODS.get(config["crossover_method"])
    mutation_fn = MUTATION_METHODS.get(config["mutation_method"])
    replacement_strategy = (config["replacement_strategy"])

    if not selection_fn or not crossover_fn or not mutation_fn:
        raise ValueError("Método de selección, crossover o mutación inválido en config.json")

    # Ejecutar generaciones
    for gen in tqdm(range(config["num_generations"]), desc="Evolucionando"):
        print(f"\nGeneración {gen + 1}/{config['num_generations']}")
        ga.run_generation(selection_fn, crossover_fn, mutation_fn, replacement_strategy)
        best = ga.get_best_individual()
        print(f"Fitness del mejor individuo: {best.fitness}")
        if (gen + 1) % 10 == 0:
            output_path = os.path.join(output_dir, f"generation_{gen+1}.png")
            print(f"Guardando progreso en: {output_path}")
            best.image.save(f"{output_path}")
        if best_fitness_threshold["threshold"] <= best.fitness:
            print(f"Condición de parada alcanzada: Fitness >= {best_fitness_threshold['threshold']}.")
            break
        else:
            if prev_best_fitness == best.fitness:
                best_fitness_threshold["tally"] += 1
            else:
                best_fitness_threshold["tally"] = 0
            prev_best_fitness = best.fitness
            if best_fitness_threshold["tally"] >= best_fitness_threshold["no_improvement_limit"]:
                print(f"Condición de parada alcanzada: El mejor fitness no ha mejorado en {best_fitness_threshold['no_improvement_limit']} generaciones.")
                break

    # Guardar el resultado final
    print("\n--- Evolución finalizada ---")
    final_best = ga.get_best_individual()
    final_output_path = os.path.join(output_dir, "final_result.png")
    
    print(f"Guardando la mejor imagen en: {final_output_path}")
    final_best.image.save(final_output_path)

    print("\n¡Proceso completado!")

if __name__ == "__main__":
    main()
