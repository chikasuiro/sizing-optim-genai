from common.ai_class import GeometryParams
from common.initialize import initialize_population
from common.beamsearch import run_optimization_beam_search
from .config import *

def mutate_params_ai(current_params: GeometryParams, simulation_result: dict, goal: str) -> GeometryParams:
    
    prompt = f'''
    あなたは熟練した計算力学エンジニアです。
    現在の設計パラメータと解析結果は以下の通りです。
    
    [現在のパラメータ]
    {current_params.model_dump_json(indent=4)}
    
    [解析結果]
    最大応力: {simulation_result['max_stress']} MPa
    体積: {simulation_result['volume']} mm^3
    
    [目標]
    {goal}
    
    物理的な考察に基づき、目標を達成するための「次の設計パラメータ」を提案してください。
    '''

    completion = client.beta.chat.completions.parse(
        model=gpt_model,
        messages=[
            {'role': 'system', 'content': 'あなたは構造最適化の専門家です。JSON形式で回答してください。'},
            {'role': 'user', 'content': prompt},
        ],
        response_format=GeometryParams,
        temperature=0.5,
    )

    return completion.choices[0].message.parsed

def main():
    dst_dir = input('作業ディレクトリを指定してください: ')
    params = {
        'length_oval': 101.000000,
        'radius': 11.000000,
        'thickness': 20.000000,
        'fillet_size': 4.00,
        'reasoning': 'オリジナルパラメーター',
    }
    initial_population = initialize_population(pop_size, GeometryParams(**params))
    run_optimization_beam_search(
        mutate_func=mutate_params_ai,
        initial_population=initial_population,
        generations=max_loop,
        beam_width=pop_size,
        goal=goal_mutate,
        dst_dir=dst_dir)

if __name__ == '__main__':
    main()
