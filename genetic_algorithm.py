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

    def _calculate_population_fitness(self):
        """Calcula el fitness para cada individuo en la población."""
        max_fitness = 0.0
        for individual in tqdm(self.population, desc="Calculando Fitness"):
            individual.calculate_fitness(self.target_image)
            if individual.fitness > max_fitness:
                max_fitness = individual.fitness
        for individual in tqdm(self.population, desc="Calculando Relative-Fitness"):
            individual.calculate_relative_fitness(max_fitness)

    def _calculate_population_ranking_pseudo_fitness(self):
        """Calcula el pseudo-fitness de ranking para cada individuo en la población."""
        sorted_population = sorted(self.population, key=lambda ind: ind.fitness, reverse=True)
        n = len(sorted_population)

        max_fitness = 0.0
        for rank, individual in enumerate(sorted_population):
            individual.pseudo_fitness = (n - (rank + 1)) / n
            if max_fitness < individual.pseudo_fitness:
                max_fitness = individual.pseudo_fitness

        for individual in sorted_population:
            individual.relative_pseudo_fitness = individual.pseudo_fitness / max_fitness
    
    def _sort_population(self):
        """Ordena la población por fitness, de mejor a peor."""
        self.population.sort(key=lambda ind: ind.fitness, reverse=True)

    def _selection_roulette(self) -> Individual:
        """Selección por Ruleta."""
        pick = random.uniform(0, 1)
        current = 0.0
        for ind in self.population:
            current += ind.relative_fitness
            if pick <= current:
                return ind
        return self.population[-1]

    def _selection_tournament(self, tournament_size: int = 5) -> Individual:
        """Selección por Torneo."""
        tournament = random.sample(self.population, tournament_size)
        return max(tournament, key=lambda ind: ind.fitness)
    
    def _selection_ranking(self) -> Individual:
        """Selección por Ranking."""
        pick = random.uniform(0, 1)
        current = 0.0
        for ind in self.population:
            current += ind.relative_pseudo_fitness
            if pick <= current:
                return ind
        return self.population[-1]
    
    # def _crossover_one_point(self, parent1: Individual, parent2: Individual) -> List[Individual]:
    #     """Cruce de un solo punto."""
    #     child1 = Individual(self.num_triangles, self.width, self.height)
    #     child2 = Individual(self.num_triangles, self.width, self.height)
        
    #     crossover_point = random.randint(1, self.num_triangles - 1)
        
    #     child1.chromosome = copy.deepcopy(parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:])
    #     child2.chromosome = copy.deepcopy(parent2.chromosome[:crossover_point] + parent1.chromosome[crossover_point:])
        
    #     return [child1, child2]

    # def _crossover_uniform(self, parent1: Individual, parent2: Individual) -> List[Individual]:
    #     """Cruce uniforme."""
    #     child1 = Individual(self.num_triangles, self.width, self.height)
    #     child2 = Individual(self.num_triangles, self.width, self.height)

    #     for i in range(self.num_triangles):
    #         if random.random() < 0.5:
    #             child1.chromosome[i] = copy.deepcopy(parent1.chromosome[i])
    #             child2.chromosome[i] = copy.deepcopy(parent2.chromosome[i])
    #         else:
    #             child1.chromosome[i] = copy.deepcopy(parent2.chromosome[i])
    #             child2.chromosome[i] = copy.deepcopy(parent1.chromosome[i])
        
    #     return [child1, child2]

    def run_generation_traditional(self):
        """Ejecuta un ciclo completo de una generación."""
        self._calculate_population_fitness()
        self._calculate_population_ranking_pseudo_fitness()
        self._sort_population()
        
        new_population = []

        """Ejecuta una generación usando reemplazo tradicional: N padres + K hijos → seleccionar N."""
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

    def run_generation(self, selection_method, crossover_method):
        """Ejecuta un ciclo completo de una generación."""
        self._calculate_population_fitness()
        self._calculate_population_ranking_pseudo_fitness()
        self._sort_population()
        
        new_population = []

        """Ejecuta una generación usando reemplazo de sesgo joven: N padres + K hijos → seleccionar N mejores."""
        #1. Generar K hijos
        while len(new_population) < self.k:
            # Seleccionar padres
            parent1 = self._selection_roulette()
            parent2 = self._selection_roulette()

            # Cruzar padres para crear hijos
            children = crossover_method(self, parent1, parent2)
            
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


    def get_best_individual(self) -> Individual:
        """Devuelve el mejor individuo de la población actual."""
        return max(self.population, key=lambda ind: ind.fitness)