import os
import heapq
from typing import List, Callable
from .ai_class import Individual, GeometryParams
from .simulate import run_simulation, calculate_score

def run_optimization_beam_search(
        mutate_func: Callable[[GeometryParams, dict, str], GeometryParams],
        initial_population: List[Individual],
        generations: int,
        beam_width: int,
        goal: str,
        dst_dir: str):

    os.chdir(dst_dir)
    current_population = initial_population
    initial_flag = True

    for gen in range(generations):
        print(f'=== Generation {gen + 1} ===')
        next_candidates = []

        for idx, parent in enumerate(current_population):
            if initial_flag:
                dirname = f'G{gen:02d}ID{idx+1:02d}'
                os.mkdir(dirname)
                os.chdir(dirname)
                result = run_simulation(params=parent.params)
                parent.score = calculate_score(result)
                parent.history += f'S -> G{gen+1:02d}ID{idx+1:02d}'
                os.chdir(os.pardir)
                initial_flag = False
            else:
                continue

            for i in range(2):
                print(f'Parent ID {idx+1} の変異ステップ {i+1}')
                new_params = mutate_func(
                    current_params=parent.params, 
                    simulation_result=result,
                    goal=goal,
                )
                print(f'AIの提案理由: {new_params.reasoning}')
                print(f'次のパラメータ: {new_params}')

                dirname = f'G{gen+1:02d}ID{idx*2+i+1:02d}'
                os.mkdir(dirname)
                os.chdir(dirname)
                new_result = run_simulation(new_params)
                score = calculate_score(new_result)
                os.chdir(os.pardir)

                child = Individual(
                    params=new_params,
                    score=score,
                    history=parent.history + f' -> G{gen+1:02d}ID{idx*2+i+1:02d}'
                )
                next_candidates.append(child)

        current_population = heapq.nlargest(beam_width, next_candidates, key=lambda x: x.score)
        print(f'Survivor indices: {[p.history[-7:] for p in current_population]}')
        print(f'Top score: {current_population[0].score}')
        print(f'Survivor Parameters: {[p.params for p in current_population]}')

    return None
