import os
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

# 環境変数を一元管理
class Config:
    SUPABASE_ARTICUL_URL = os.getenv("SUPABASE_ARTICUL_URL")
    SUPABASE_ARTICUL_KEY = os.getenv("SUPABASE_ARTICUL_KEY")
