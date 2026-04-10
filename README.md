# sizing-optim-genai
Sample code for sizing optimization problem with GenAI

## Usage (for external)

1. リポジトリをクローンする

```powershell
git clone https://github.com/chikasuiro/sizing-optim-genai.git
cd sizing-optim-genai
```

2. OpenAIまたはGoogleのAPIキーを取得する
3. `.env`にAPIキーを設定する
4. 仮想環境を作成し、必要なモジュールをインストールする

```powershell
uv venv  # if you use uv
.venv\Scripts\activate
uv pip install -U dotenv openai google-genai
```

5. 本プロジェクトのルートディレクトリを`PYTHONPATH`に追加する

```powershell
$env:PYTHONPATH = "C:\Users\path\to\sizing-optim-genai\;" + $env:PYTHONPATH
```

6. `external`ディレクトリに移動する

```powershell
cd external
```

7. `config.py`に、モデル・ゴールの文言などを設定する
8. `ai_mutate.py`を実行する

```powershell
python ai_mutate.py
```

## Note

形状・寸法は、[ミスミ 型開き防止プレート -切り欠き全長指定タイプ-](https://jp.misumi-ec.com/vona2/detail/110200110620/)を利用した
