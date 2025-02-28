"""
    動作に必要なAPIKEYやURLを環境変数から設定する
"""
import os
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

# 環境変数を一元管理
class Config:
    SUPABASE_ARTICUL_URL = os.getenv("SUPABASE_ARTICUL_URL")
    SUPABASE_ARTICUL_KEY = os.getenv("SUPABASE_ARTICUL_KEY")
    SUPABASE_CHAT_URL = os.getenv("SUPABASE_CHAT_URL")
    SUPABASE_CHAT_KEY = os.getenv("SUPABASE_CHAT_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
