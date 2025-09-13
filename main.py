# main.py
import json
from PIL import Image
from genetic_algorithm import GeneticAlgorithm
from selection import boltzmann, elitist, ranking, roulette, tournament_deterministic, tournament_probabilistic
from crossover import anular, one_point, two_point, uniform

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

def main():
    config = load_config()

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

    if not selection_fn or not crossover_fn:
        raise ValueError("Método de selección o crossover inválido en config.json")

    # Ejecutar generaciones
    for gen in range(config["num_generations"]):
        print(f"\nGeneración {gen + 1}/{config['num_generations']}")
        ga.calculate_population_fitness(ga.population)
        ga.run_generation(selection_fn, crossover_fn)
        best = ga.get_best_individual()
        print(f"Fitness del mejor individuo: {best.fitness}")

if __name__ == "__main__":
    main()
