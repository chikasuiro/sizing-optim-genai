import os
from openai import OpenAI
from pydantic import BaseModel
from typing import List

# APIキーの設定（環境変数から読み込むのが安全です）
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class SelectionResult(BaseModel):
    selected_id: int
    justification: str

def select_best_design(candidates: List[dict], user_preference: str) -> SelectionResult:
    
    # 候補リストを文字列化してプロンプトに埋め込む
    candidates_str = "\n".join([f"ID:{c['id']}, 応力:{c['stress']}, 重量:{c['weight']}" for c in candidates])
    
    prompt = f"""
    以下の設計候補（パレート解）の中から、ユーザーの要望に最も合致するものを1つ選んでください。
    
    [候補リスト]
    {candidates_str}
    
    [ユーザーの要望]
    "{user_preference}"
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o", 
        messages=[
            {"role": "system", "content": "あなたはプロジェクトマネージャーです。最適な設計案を選定してください。"},
            {"role": "user", "content": prompt},
        ],
        response_format=SelectionResult,
    )

    return completion.choices[0].message.parsed

# --- 実行例 ---
pareto_front = [
    {"id": 1, "stress": 200, "weight": 50},
    {"id": 2, "stress": 150, "weight": 80},
    {"id": 3, "stress": 100, "weight": 120},
]

decision = select_best_design(pareto_front, "多少重くなってもいいから、とにかく安全な（応力が低い）ものがいい")

print(f"AIが選んだID: {decision.selected_id}")
print(f"理由: {decision.justification}")
