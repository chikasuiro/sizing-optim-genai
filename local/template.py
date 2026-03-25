import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
from pydantic import BaseModel

# --- モデルのロード（初回のみ実行されるようにグローバル等で管理推奨） ---
model_id = "Qwen/Qwen2.5-7B-Instruct"  # おすすめモデル（後述）

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto"  # GPUがあれば自動で使用
)

# 定義クラス（変更なし）
class GeometryParams(BaseModel):
    length: float
    thickness: float
    fillet_radius: float
    reasoning: str

# --- ローカルLLM呼び出し関数 ---
def mutate_by_local_llm(current_params: dict, simulation_result: dict, goal: str) -> GeometryParams:
    
    # 1. プロンプト作成（JSONを出力するように明示的な指示を追加）
    prompt_content = f"""
    あなたは熟練した計算力学エンジニアです。
    以下の設計目標を達成するための「次の設計パラメータ」を検討し、JSON形式のみを出力してください。
    余計な解説やMarkdownのバッククォート(```)は不要です。

    [現在のパラメータ]
    {current_params}
    
    [解析結果]
    最大応力: {simulation_result['max_stress']} MPa
    体積: {simulation_result['volume']} mm^3
    
    [目標]
    {goal}
    
    [出力フォーマット(JSON)]
    {{
        "length": <float>,
        "thickness": <float>,
        "fillet_radius": <float>,
        "reasoning": "<string: 変更理由>"
    }}
    """

    messages = [
        {"role": "system", "content": "You are a helpful assistant. You answer in JSON format only."},
        {"role": "user", "content": prompt_content}
    ]

    # 2. 推論実行
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512,
        temperature=0.7, # ここで温度指定
        do_sample=True   # temperatureを有効にするためTrue
    )
    
    # プロンプト部分を除去して回答のみ取得
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    # 3. JSONパースとエラーハンドリング
    try:
        # Markdownのコードブロックが含まれてしまう場合の除去処理
        clean_text = response_text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_text)
        return GeometryParams(**data)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSONパースエラー: {e}")
        print(f"モデルの生出力: {response_text}")
        # エラー時は現状維持などを返すか、再試行ロジックを入れる
        return GeometryParams(**current_params, reasoning="Error in generation")

# --- 実行部分は同じ ---
