# mutation_methods.py
from individual import Individual

def basic_mutation(individual: Individual, mutation_rate):
    individual.mutate_gene(mutation_rate)

def multigen_uniform_mutation(individual: Individual, mutation_rate):
    individual.mutate_multigen_uniform(mutation_rate)

def complete_mutation(individual: Individual, mutation_rate):
    individual.mutate_complete(mutation_rate)
