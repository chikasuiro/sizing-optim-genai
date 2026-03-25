import os
from openai import OpenAI
from pydantic import BaseModel
from typing import List

# APIキーの設定（環境変数から読み込むのが安全です）
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 1. 出力してほしいデータ構造を定義（Pydanticを使用）
class GeometryParams(BaseModel):
    length: float
    thickness: float
    fillet_radius: float
    reasoning: str  # なぜその値を提案したかの理由も出力させる

# 2. 既存の解析フロー（ダミー関数）
def run_simulation(params: GeometryParams):
    # ここでCAD変更 -> メッシュ -> ソルバー -> 結果取得 を行う
    # 今回はダミーの結果を返します
    print(f"解析実行: {params}")
    return {"max_stress": 120.0, "volume": 500.0}

# 3. LLMによる変異関数（Optimizer）
def mutate_by_llm(current_params: dict, simulation_result: dict, goal: str) -> GeometryParams:
    
    prompt = f"""
    あなたは熟練した計算力学エンジニアです。
    現在の設計パラメータと解析結果は以下の通りです。
    
    [現在のパラメータ]
    {current_params}
    
    [解析結果]
    最大応力: {simulation_result['max_stress']} MPa
    体積: {simulation_result['volume']} mm^3
    
    [目標]
    {goal}
    
    物理的な考察に基づき、目標を達成するための「次の設計パラメータ」を提案してください。
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",  # 高精度な推論が必要なため4oを推奨
        messages=[
            {"role": "system", "content": "あなたは構造最適化の専門家です。JSON形式で回答してください。"},
            {"role": "user", "content": prompt},
        ],
        response_format=GeometryParams, # ここで型を指定して強制的にJSON化
        temperature=0.5,  # ここに追加（0.0〜2.0）
    )

    return completion.choices[0].message.parsed

# --- 実行フローの例 ---
current_design = {"length": 100, "thickness": 5, "fillet_radius": 2}
result = run_simulation(GeometryParams(**current_design))

# 応力が高いので下げたい、という指示でLLMを呼び出す
new_design_obj = mutate_by_llm(
    current_params=current_design,
    simulation_result=result,
    goal="最大応力を100MPa以下に抑えつつ、体積増加は最小限にしたい。応力集中を緩和する形状にして。"
)

print("-" * 30)
print(f"AIの提案理由: {new_design_obj.reasoning}")
print(f"次のパラメータ: L={new_design_obj.length}, T={new_design_obj.thickness}, R={new_design_obj.fillet_radius}")
