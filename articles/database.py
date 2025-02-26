from flask import Blueprint, request, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import supabase

# .env ファイルを読み込む
load_dotenv()

# 環境変数を取得
SUPABASE_ARTICUL_URL  = os.getenv("SUPABASE_ARTICUL_URL")
SUPABASE_ARTICUL_KEY = os.getenv("SUPABASE_ARTICUL_KEY")

supabase: Client = create_client(SUPABASE_ARTICUL_URL, SUPABASE_ARTICUL_KEY)

# 記事の追加
def add_article(data):
    
    title = data.get("title")
    article_body = data.get("article_body")
    user_name = data.get("user_name")

    if not title or not article_body or not user_name:
        return jsonify({"error": "title, article_body, user_name are required"}), 400

    response = supabase.table("articles").insert({
        "title": title,
        "article_body": article_body,
        "user_name": user_name
    }).execute()
    
    return jsonify(response.data), 201


# とりあえず全部読む。設計によって取り出す範囲や内容を後に決定
# 記事のタイトルのみを読み取る
def get_article_title():
    # titles というカラム名が "title" であれば下記のとおり
    # すべての行の "title" カラムだけを取得
    response = supabase.table("articles").select("title").execute()
    return jsonify(response.data), 200

# 記事の全文を読み取る
def get_article():
    # すべてのカラムを取得する場合は select("*")
    response = supabase.table("articles").select("*").execute()
    return jsonify(response.data), 200