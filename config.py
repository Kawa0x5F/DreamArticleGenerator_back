import os
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

# 環境変数を一元管理
class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
