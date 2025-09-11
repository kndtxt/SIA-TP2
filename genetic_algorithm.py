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
from multiprocessing import Pool, cpu_count

def setup_logging(config_path="config/logger.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    logging.config.dictConfig(config)

# worker para multiprocessing
from individual import Individual

def _eval_individual(idx, chromosome, width, height, num_triangles, target_image):
    """
    Reconstruye un Individual en el worker, calcula fitness y lo devuelve.
    """
    ind = Individual(num_triangles, width, height)
    ind.chromosome = chromosome  # reusamos los triángulos ya generados
    ind._image = None            # limpiar caché de imagen
    ind.calculate_fitness(target_image)
    return idx, ind.fitness


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
        self.generation = 0
        self.workers = getattr(self, "workers", os.cpu_count())
        setup_logging()
        self.logger = logging.getLogger(__name__)
        
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

    def _selection_roulette(self, quantity: int) -> list[Individual]:
        """Selección por Ruleta."""
        picks: list[Individual] = []
        current = 0.0
        for k in range(quantity):
            pick = random.uniform(0, 1)
            for ind in self.population:
                current += ind.relative_fitness
                if pick <= current:
                    picks.append(ind)
                    break
        return picks
    
    def _selection_universal(self, quantity: int) -> list[Individual]:
        """Selección Universal."""
        if quantity == 0:
            return None
        picks: list[Individual] = []
        pick = random.uniform(0, 1)
        for k in range(quantity):
            current_pick = (pick + (k-1))/quantity
            current = 0.0
            for ind in self.population:
                current += ind.relative_fitness
                if current_pick <= current:
                    picks.append(ind)
                    break
        return picks
    
    def _selection_ranking(self) -> Individual:
        """Selección por Ranking."""
        pick = random.uniform(0, 1)
        current = 0.0
        for ind in self.population:
            current += ind.relative_pseudo_fitness
            if pick <= current:
                return ind
        return self.population[-1]

    def _selection_tournament_deterministic(self, tournament_size: int, quantity: int) -> list[Individual]:
        """Selección por Torneo Deterministico."""
        picks: list[Individual] = []
        for _ in range(quantity):
            tournament = random.sample(self.population, tournament_size)
            picks.append(max(tournament, key=lambda ind: ind.fitness))
        return picks
    
    def _selection_tournament_probabilistic(self, quantity: int) -> list[Individual]:
        """Selección por Torneo Probabilistico."""
        picks: list[Individual] = []
        threshold = 0.9
        for _ in range(quantity):
            r = random.uniform(0, 1)
            tournament = random.sample(self.population, 2)
            if r < threshold:
                picks.append(max(tournament, key=lambda ind: ind.fitness))
            else:
                picks.append(min(tournament, key=lambda ind: ind.fitness))
        return picks
    
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
            # Puedes cambiar a _crossover_uniform aquí para probar
            children = Crossover()._crossover_one_point(parent1, parent2, self.width, self.height, self.num_triangles)

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
            parents = self._selection_tournament_probabilistic(2)

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


    def get_best_individual(self) -> Individual:
        """Devuelve el mejor individuo de la población actual."""
        return max(self.population, key=lambda ind: ind.fitness)
    

    ## Paralelización de la creación de descendencia

    def _make_children_task(self, args):
        (p1, p2,  width, height, ntri, crossover_type, mutation_rate, seed) = args
        rng = random.Random(seed)

        cross = Crossover()
        if crossover_type == "uniform":
            kids = cross._crossover_uniform(p1, p2, width, height, ntri)
        else:
            kids = cross._crossover_one_point(p1, p2, width, height, ntri)

        out = []
        for c in kids:
            if rng.random() < mutation_rate:
                c.mutate_gene()        
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