# genetic_algorithm.py
import random
import copy
from typing import List
from tqdm import tqdm # Para la barra de progreso
from individual import Individual

class GeneticAlgorithm:
    """
    Motor del algoritmo genético para evolucionar imágenes.
    """
    def __init__(self, target_image, pop_size: int, num_triangles: int, 
                 elitism_count: int, mutation_rate: float):
        self.target_image = target_image
        self.width, self.height = target_image.size
        self.pop_size = pop_size
        self.num_triangles = num_triangles
        self.elitism_count = elitism_count
        self.mutation_rate = mutation_rate
        
        print("Inicializando población...")
        self.population: List[Individual] = [
            Individual(num_triangles, self.width, self.height) 
            for _ in tqdm(range(pop_size))
        ]

    def _calculate_population_fitness(self):
        """Calcula el fitness para cada individuo en la población."""
        for individual in tqdm(self.population, desc="Calculando Fitness"):
            individual.calculate_fitness(self.target_image)
    
    def _sort_population(self):
        """Ordena la población por fitness, de mejor a peor."""
        self.population.sort(key=lambda ind: ind.fitness, reverse=True)

    def _selection_roulette(self) -> Individual:
        """Selección por Ruleta."""
        total_fitness = sum(ind.fitness for ind in self.population)
        pick = random.uniform(0, total_fitness)
        current = 0
        for ind in self.population:
            current += ind.fitness
            if current > pick:
                return ind
        return self.population[-1]

    def _selection_tournament(self, tournament_size: int = 5) -> Individual:
        """Selección por Torneo."""
        tournament = random.sample(self.population, tournament_size)
        return max(tournament, key=lambda ind: ind.fitness)
    
    def _crossover_one_point(self, parent1: Individual, parent2: Individual) -> List[Individual]:
        """Cruce de un solo punto."""
        child1 = Individual(self.num_triangles, self.width, self.height)
        child2 = Individual(self.num_triangles, self.width, self.height)
        
        crossover_point = random.randint(1, self.num_triangles - 1)
        
        child1.chromosome = copy.deepcopy(parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:])
        child2.chromosome = copy.deepcopy(parent2.chromosome[:crossover_point] + parent1.chromosome[crossover_point:])
        
        return [child1, child2]

    def _crossover_uniform(self, parent1: Individual, parent2: Individual) -> List[Individual]:
        """Cruce uniforme."""
        child1 = Individual(self.num_triangles, self.width, self.height)
        child2 = Individual(self.num_triangles, self.width, self.height)

        for i in range(self.num_triangles):
            if random.random() < 0.5:
                child1.chromosome[i] = copy.deepcopy(parent1.chromosome[i])
                child2.chromosome[i] = copy.deepcopy(parent2.chromosome[i])
            else:
                child1.chromosome[i] = copy.deepcopy(parent2.chromosome[i])
                child2.chromosome[i] = copy.deepcopy(parent1.chromosome[i])
        
        return [child1, child2]

    def run_generation(self):
        """Ejecuta un ciclo completo de una generación."""
        self._calculate_population_fitness()
        self._sort_population()
        
        new_population = []

        # 1. Elitismo: Los mejores individuos pasan directamente
        for i in range(self.elitism_count):
            new_population.append(self.population[i])

        # 2. Creación de nueva descendencia
        while len(new_population) < self.pop_size:
            # Seleccionar padres
            parent1 = self._selection_tournament()
            parent2 = self._selection_tournament()
            
            # Cruzar padres para crear hijos
            # Puedes cambiar a _crossover_uniform aquí para probar
            children = self._crossover_one_point(parent1, parent2)
            
            # Mutar hijos
            for child in children:
                if random.random() < self.mutation_rate:
                    child.mutate_gene()
                if len(new_population) < self.pop_size:
                    new_population.append(child)
        
        self.population = new_population

    def get_best_individual(self) -> Individual:
        """Devuelve el mejor individuo de la población actual."""
        return max(self.population, key=lambda ind: ind.fitness)