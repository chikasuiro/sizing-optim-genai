from typing import List
from .ai_class import Individual

def initialize_population(size: int, initial_params: dict) -> List[Individual]:
    population = []
    for _ in range(size):
        individual = Individual(
            params=initial_params,
            score=0.0,
            history=''
        )
        population.append(individual)
    return population
