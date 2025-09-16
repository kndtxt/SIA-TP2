# genetic_algorithm.py
import random
from typing import List
from tqdm import tqdm # Para la barra de progreso
from individual import Individual
import multiprocessing
import json

with open('./configs/config.json') as f:
    config = json.load(f)
    selection_method_config = config["selection_method"]
class GeneticAlgorithm:
    """
    Motor del algoritmo genético para evolucionar imágenes.
    """
    def __init__(self, target_image, pop_size: int, k: int, num_triangles: int, mutation_rate: float):
        self.target_image = target_image
        self.width, self.height = target_image.size
        self.pop_size = pop_size
        self.k = k
        self.num_triangles = num_triangles
        self.mutation_rate = mutation_rate
        
        print("Inicializando población...")
        self.population: List[Individual] = [
            Individual(num_triangles, self.width, self.height) 
            for _ in tqdm(range(pop_size))
        ]



    # calculo del fitness con multiprocesamiento
    def _calculate_individual_fitness(self, individual_data):
        """Función auxiliar para calcular el fitness de un individuo (para multiprocesamiento)."""
        individual, target_image = individual_data
        individual.calculate_fitness(target_image)
        return individual

    def calculate_population_fitness(self, population: List['Individual']):
        """Calcula el fitness para cada individuo en la población usando multiprocessing."""
        data = [(individual, self.target_image) for individual in population]
        num_workers = max(1, multiprocessing.cpu_count() - 2)
        with multiprocessing.Pool(processes=num_workers) as pool:
            results = list(tqdm(pool.imap(self._calculate_individual_fitness, data), total=len(population), desc="Calculando Fitness"))
        total_fitness = sum(ind.fitness for ind in results)
        for ind in results:
            ind.relative_fitness = ind.fitness / total_fitness if total_fitness > 0 else 0
        for i, ind in enumerate(results):
            population[i].fitness = ind.fitness
            population[i].relative_fitness = ind.relative_fitness
    
    def _sort_population(self):
        """Ordena la población por fitness, de mejor a peor."""
        self.population.sort(key=lambda ind: ind.fitness, reverse=True)

    def run_generation(self, selection, crossover, mutation, replacement_strategy, generation_selection, generation=None):
        """
        Ejecuta un ciclo completo de una generación.
        """

        print("selection_fn:", selection)

        new_population = []

        # Creación de nueva descendencia k
        if(generation is not None):
            parents = selection(self, self.population, self.k, generation)
        else:
            parents = selection(self, self.population, self.k)
        children = crossover(self, parents)
        children = children[:self.k]

        print(f"[DEBUG] Cantidad de padres: {len(parents)}")
        print(f"[DEBUG] Hijos generados: {len(children)}")

        # Mutación de la descendencia
        for child in children:
                if random.random() < self.mutation_rate:
                    mutation(child, self.mutation_rate)

        # Selección de la siguiente generación
        new_population = children

        if(replacement_strategy == "traditional"):
            # 2. Combinar padres + hijos
            combined_population = self.population + new_population

            # 3. Ordenar por fitness y seleccionar N al azar
            self.population = generation_selection(self, combined_population, self.pop_size)
            self.calculate_population_fitness(self.population)

        else:
            if(replacement_strategy == "young_bias"):
                # 2. K > N
                if self.k > self.pop_size:
                    self.population = generation_selection(self, new_population, self.pop_size)
                    self.calculate_population_fitness(self.population)
                #3. K <= N
                else:
                    old_population = generation_selection(self, self.population, self.pop_size - self.k)
                    self.population = new_population + old_population
                    self.calculate_population_fitness(self.population)
            else:
                raise ValueError(f"Estrategia de reemplazo inválida: {replacement_strategy}")
        

    def get_best_individual(self) -> Individual:
        """Devuelve el mejor individuo de la población actual."""
        return max(self.population, key=lambda ind: ind.fitness)