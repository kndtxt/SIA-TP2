# genetic_algorithm.py
import random
from typing import List
from tqdm import tqdm # Para la barra de progreso
from individual import Individual

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

    def calculate_population_fitness(self, population: List[Individual]):
        """Calcula el fitness para cada individuo en la población."""
        total_fitness = 0.0
        for individual in tqdm(population, desc="Calculando Fitness"):
            individual.calculate_fitness(self.target_image)
            total_fitness += individual.fitness
        for individual in population:
            individual.relative_fitness = individual.fitness/total_fitness
    
    def _sort_population(self):
        """Ordena la población por fitness, de mejor a peor."""
        self.population.sort(key=lambda ind: ind.fitness, reverse=True)

    def run_generation(self, selection, crossover, mutation, replacement_strategy):
        """Ejecuta un ciclo completo de una generación."""
        
        new_population = []

        # Creación de nueva descendencia k
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
            self.population = selection(self, combined_population, self.pop_size)
            self.calculate_population_fitness(self.population)

        else:
            if(replacement_strategy == "young_bias"):
                # 2. K > N
                if self.k > self.pop_size:
                    self.population = selection(self, new_population, self.pop_size)
                    self.calculate_population_fitness()
                #3. K <= N
                else:
                    old_population = selection(self, self.population, self.pop_size - self.k)
                    self.population = new_population + old_population
                    self.calculate_population_fitness()
            else:
                raise ValueError(f"Estrategia de reemplazo inválida: {replacement_strategy}")
        

    def get_best_individual(self) -> Individual:
        """Devuelve el mejor individuo de la población actual."""
        return max(self.population, key=lambda ind: ind.fitness)