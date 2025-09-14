# genetic_algorithm.py
import random
from typing import List, Callable
from tqdm import tqdm # Para la barra de progreso
from individual import Individual
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def mutate_child(child, mutation_rate, mutation_fn):
        if random.random() < mutation_rate:
            mutation_fn(child, mutation_rate)
        return child

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
        total_fitness = 0.0

        with ThreadPoolExecutor() as executor:
            list(tqdm(executor.map(lambda ind: ind.calculate_fitness(self.target_image), population),
                    total=len(population), desc="Calculando Fitness"))
        
        total_fitness = sum(ind.fitness for ind in population)

        for individual in population:
            individual.calculate_relative_fitness(total_fitness)
 
    def sort_population(population: List[Individual]):
        """Ordena la población por fitness, de mejor a peor."""
        population.sort(key=lambda ind: ind.fitness, reverse=True)
    
    def get_best_individual(self) -> Individual:
        """Devuelve el mejor individuo de la población actual."""
        return max(self.population, key=lambda ind: ind.fitness)

    def run_generation(self, selection_method: Callable, crossover_method: Callable, mutation_method, replacement_strategy: str):
        """Ejecuta un ciclo completo de una generación."""
        new_population = []

        """Ejecuta una generación usando reemplazo de sesgo joven: N padres + K hijos → seleccionar N mejores."""
        #1. Generar K hijos
        # Seleccionar padres
        num_pairs = (self.k + 1) // 2  # ceil(k/2)
        parent_pairs = [
            selection_method(self, self.population, 2)
            for _ in range(num_pairs)
        ]

        # Cruzar padres para crear hijos
        children = []
        for p1, p2 in parent_pairs:
            children.extend(crossover_method(self, p1, p2))
        
        children = children[:self.k]
            
        # Mutar hijos
        with ThreadPoolExecutor() as executor:
            children = list(executor.map(lambda child: mutate_child(child, self.mutation_rate, mutation_method),children))

        new_population = children

        if(replacement_strategy == "traditional"):
            # 2. Combinar padres + hijos
            combined_population = self.population + new_population

            # 3. Ordenar por fitness y seleccionar N al azar
            self.population = selection_method(self, combined_population, self.pop_size)

        else:
            if(replacement_strategy == "young_bias"):
                # 2. K > N
                if self.k > self.pop_size:
                    self.population = selection_method(self, new_population, self.pop_size)
                #3. K <= N
                else:
                    old_population = selection_method(self, self.population, self.pop_size - self.k)
                    self.population = new_population + old_population
            else:
                raise ValueError(f"Estrategia de reemplazo inválida: {replacement_strategy}")