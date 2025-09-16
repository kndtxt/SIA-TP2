import json
import matplotlib.pyplot as plt
import os
import sys


# Cargar configuración desde JSON
def load_config(path="./configs/config.json"):
    with open(path, "r") as file:
        return json.load(file)

def load_file(path):
    with open(path, "r") as file:
        return file.read()

best_fitness_threshold = {
    "threshold": 0.05,
    "no_improvement_limit": 100,
    "tally": 0
}

def fitness_over_generations():
    file = load_file("./metrics/fitness_log.txt")
    lines = file.split("\n")
    generations = []
    fitness_values = []
    for line in lines[1:]:  # Saltar la primera línea (encabezado)
        if line:
            generation, fitness = line.split(";")
            generations.append(int(generation))
            fitness_values.append(float(fitness))
    plt.plot(generations, fitness_values, label="Fitness over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Fitness over Generations")
    plt.legend()
    plt.savefig(f'./metrics/graphs/{sys.argv[0]}.png')


def main():
    config = load_config()
    best_fitness_threshold["threshold"] = config.get("FITNESS_THRESHOLD", best_fitness_threshold["threshold"])
    print(best_fitness_threshold)
    if not os.path.exists("./metrics/graphs"):
        os.makedirs("./metrics/graphs")
    fitness_over_generations()
main()
