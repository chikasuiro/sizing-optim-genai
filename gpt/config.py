import os
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai

load_dotenv(os.pardir + '/.env')

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
gpt_model = 'gpt-4o'
gemini_model = 'gemini-1.5-flash'
gemini_flag = True

pop_size = 3
max_loop = 30
goal_mutate = '最大応力を0.2 MPa以下に抑えつつ、体積増加は最小限にしたい。応力集中を緩和する形状にして。'
goal_result = '多少重くなってもいいから、とにかく安全な（応力が低い）ものがいい。'
