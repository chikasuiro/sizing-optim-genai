import heapq
from typing import List
from pydantic import BaseModel

class GeometryParams(BaseModel):
    length: float
    thickness: float
    fillet_radius: float
    reasoning: str  # なぜその値を提案したかの理由も出力させる

# データ構造（前回のGeometryParamsに解析結果を含めたもの）
class Individual(BaseModel):
    params: GeometryParams
    score: float  # 適応度（例: -1 * 応力 など、高いほど良いとする）
    history: str  # どのような変更を経てきたかのログ

def run_optimization_beam_search(initial_population: List[Individual], generations: int, beam_width: int):
    
    current_population = initial_population
    
    for gen in range(generations):
        print(f"=== Generation {gen + 1} ===")
        next_candidates = []
        
        # 1. 現世代の各個体について、LLMに改善案を出させる
        for parent in current_population:
            # 1つの親から2つの異なる改善案を出させてみる（多様性確保）
            for i in range(2): 
                # 【ポイント】temperatureを少し上げて(0.7〜0.9)多様な案を出させる
                new_params = mutate_by_llm(
                    current_params=parent.params, 
                    simulation_result=get_sim_result(parent), # 擬似関数
                    goal="剛性を維持しつつ軽量化",
                    temperature=0.8 
                )
                
                # 解析実行
                sim_res = run_simulation(new_params)
                score = calculate_score(sim_res) # 目的関数
                
                child = Individual(
                    params=new_params,
                    score=score,
                    history=parent.history + f" -> G{gen}_Var{i}"
                )
                next_candidates.append(child)
        
        # 2. 選択 (Selection): 成績上位 beam_width 個（例: 3個）だけを残す
        # keyはscoreが大きい順
        current_population = heapq.nlargest(beam_width, next_candidates, key=lambda x: x.score)
        
        # ログ出力
        print(f"Top score: {current_population[0].score}")
        print(f"Survivor Parameters: {[p.params for p in current_population]}")

    return current_population[0]
