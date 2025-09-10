# genetic_algorithm.py
import random
import copy
import os
from typing import List
from tqdm import tqdm # Para la barra de progreso
from individual import Individual
import logging
import logging.config
import json
from crossover.crossover_class import Crossover
from concurrent.futures import ThreadPoolExecutor, as_completed

def setup_logging(config_path="config/logger.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    logging.config.dictConfig(config)


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
        self.generation = 0
        self.workers = getattr(self, "workers", os.cpu_count())
        setup_logging()
        self.logger = logging.getLogger(__name__)
        
        print("Inicializando población...")
        self.population: List[Individual] = [
            Individual(num_triangles, self.width, self.height) 
            for _ in tqdm(range(pop_size))
        ]

    # def _calculate_population_fitness(self):
    #     """Calcula el fitness para cada individuo en la población."""
    #     with ThreadPoolExecutor(max_workers=self.workers) as ex:
    #         futures = [
    #             ex.submit(individual.calculate_fitness, self.target_image)
    #             for individual in self.population
    #         ]
    #         # tqdm sobre as_completed para mantener la barra de progreso
    #         for _ in tqdm(as_completed(futures), total=len(futures), desc="Calculando Fitness (threads)"):
    #             pass
    
    def _calculate_population_fitness(self):
        """Calcula el fitness y relative fitness para cada individuo en la población usando threads."""
        # Calcular fitness en paralelo
        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futures = [
                ex.submit(individual.calculate_fitness, self.target_image)
                for individual in self.population
            ]
            for _ in tqdm(as_completed(futures), total=len(futures), desc="Calculando Fitness (threads)"):
                pass

        # Obtener el fitness máximo
        max_fitness = max(ind.fitness for ind in self.population)
        self.logger.debug(f"Max fitness en la población: {max_fitness}")

        # Calcular relative fitness en paralelo
        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futures = [
                ex.submit(individual.calculate_relative_fitness, max_fitness)
                for individual in self.population
            ]
            for _ in tqdm(as_completed(futures), total=len(futures), desc="Calculando Relative-Fitness (threads)"):
                pass

    def _sort_population(self):
        """Ordena la población por fitness, de mejor a peor."""
        self.population.sort(key=lambda ind: ind.fitness, reverse=True)

    def _selection_roulette(self) -> Individual:
        """Selección por Ruleta."""
        total_fitness = sum(ind.fitness for ind in self.population)
        self.logger.debug(f"Total fitness: {total_fitness}")
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
    
    def _make_children_task(self, args):
        (p1, p2,  width, height, ntri, crossover_type, mutation_rate, seed) = args
        rng = random.Random(seed)  # RNG local por tarea (reproducible)

        cross = Crossover()
        if crossover_type == "uniform":
            kids = cross._crossover_uniform(p1, p2, width, height, ntri)
        else:
            kids = cross._crossover_one_point(p1, p2, width, height, ntri)

        out = []
        for c in kids:
            if rng.random() < mutation_rate:
                c.mutate_gene()        # mutación dentro de la tarea (sin compartir estado externo)
            out.append(c)
        return out  # [child1, child2]

    def _offspring_parallel(self, needed: int) -> List[Individual]:
        # Pre-armo las tareas con selección en el hilo principal
        tasks = []
        pairs = (needed + 1) // 2
        base_seed = (getattr(self, "seed", 12345) ^ (self.generation << 16))

        for i in range(pairs):
            p1 = self._selection_tournament()
            p2 = self._selection_tournament()

            self.logger.debug(f"Selected parents for pair {i}: Fitness {p1.fitness}, {p2.fitness}")

            tasks.append((
                p1, p2,
                self.width, self.height, self.num_triangles,
                getattr(self, "crossover_type", "one_point"),
                self.mutation_rate,
                base_seed + i
            ))

        children = []
        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futures = [ex.submit(self._make_children_task, t) for t in tasks]
            for fut in as_completed(futures):
                children.extend(fut.result())

        return children[:needed]


    def run_generation(self):
        """Ejecuta un ciclo completo de una generación."""
        self._calculate_population_fitness()
        self._sort_population()
        
        new_population = []

        # 1. Elitismo: Los mejores individuos pasan directamente
        for i in range(self.elitism_count):
            new_population.append(self.population[i]) # ver de poner clones

        # 2. Creación de nueva descendencia
        need = self.pop_size - len(new_population)
        if need > 0:
            children = self._offspring_parallel(need)
            new_population.extend(children)

        # while len(new_population) < self.pop_size:
        #     # Seleccionar padres
        #     parent1 = self._selection_tournament()
        #     parent2 = self._selection_tournament()
            
        #     # Cruzar padres para crear hijos
        #     # Puedes cambiar a _crossover_uniform aquí para probar
        #     children = Crossover()._crossover_one_point(parent1, parent2, self.width, self.height, self.num_triangles)

        #     # Mutar hijos
        #     for child in children:
        #         if random.random() < self.mutation_rate:
        #             child.mutate_gene()
        #         if len(new_population) < self.pop_size:
        #             new_population.append(child)
        
        self.population = new_population
        self.generation += 1

    def get_best_individual(self) -> Individual:
        """Devuelve el mejor individuo de la población actual."""
        return max(self.population, key=lambda ind: ind.fitness)