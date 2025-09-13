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
            individual.calculate_relative_fitness(total_fitness)
 
    def sort_population(population: List[Individual]):
        """Ordena la población por fitness, de mejor a peor."""
        population.sort(key=lambda ind: ind.fitness, reverse=True)
    
    def get_best_individual(self) -> Individual:
        """Devuelve el mejor individuo de la población actual."""
        return max(self.population, key=lambda ind: ind.fitness)

    """
    def run_generation_traditional(self):
        #Ejecuta un ciclo completo de una generación.
        new_population = []

        #Ejecuta una generación usando reemplazo tradicional: N padres + K hijos → seleccionar N.
        #1. Generar K hijos
        while len(new_population) < self.k:
            # Seleccionar padres
            parent1 = self._selection_roulette()
            parent2 = self._selection_roulette()

            # Cruzar padres para crear hijos
            children = self._crossover_one_point(parent1, parent2)
            
            # Mutar hijos
            for child in children:
                if random.random() < self.mutation_rate:
                    child.mutate_gene()
                if len(new_population) < self.k:
                    new_population.append(child)

        # 2. Combinar padres + hijos
        combined_population = self.population + new_population

        # 3. Ordenar por fitness y seleccionar N al azar
        self.population = random.sample(combined_population, self.pop_size)
    """

    def run_generation(self, selection_method, crossover_method):
        """Ejecuta un ciclo completo de una generación."""
        new_population = []

        """Ejecuta una generación usando reemplazo de sesgo joven: N padres + K hijos → seleccionar N mejores."""
        #1. Generar K hijos
        while len(new_population) < self.k:
            # Seleccionar padres
            parents = selection_method(self, self.population, 2)

            # Cruzar padres para crear hijos
            children = crossover_method(self, parents[0], parents[1])
            
            # Mutar hijos
            for child in children:
                if random.random() < self.mutation_rate:
                    child.mutate_gene()
                if len(new_population) < self.k:
                    new_population.append(child)

        # 2. K > N
        if self.k > self.pop_size:
            self.population = random.sample(new_population, self.pop_size)
        #3. K <= N
        else:
            old_population = random.sample(self.population, self.pop_size - self.k)
            self.population = new_population + old_population
        return