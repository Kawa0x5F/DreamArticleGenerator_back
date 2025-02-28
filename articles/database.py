"""
    記事に関する処理と,それに付随するDBとの処理を行う
"""
from flask import jsonify
from supabase import create_client, Client
import supabase
from datetime import datetime, timezone, timedelta
from config import Config
from articles.generate_summary import content_to_summary

# データベースへのアクセス用のクライアントを作成
supabase: Client = create_client(
    Config.SUPABASE_ARTICUL_URL, Config.SUPABASE_ARTICUL_KEY
    )

def add_article(data):
    """
        記事をデータベースに保存する
    """

    # クライアントから渡されたデータを取得する
    title = data.get("title")               # タイトルを取得
    content = data.get("content")           # 記事の本文を取得
    summary = content_to_summary(content)   # 記事の要約を取得
    author = data.get("author")             # 記事の作成者を取得
    timestamp = datetime.now(timezone(timedelta(hours=9))).strftime("%Y年%m月%d日") # 作成日を取得

    if not title or not content or not author:
        return jsonify({"error": "title, content, author are required"}), 400
    
    response = supabase.table("articles").insert({
        "title": title,
        "content": content,
        "summary": summary,
        "author": author,
        "timestamp": [timestamp]  # `text[]` 型の `time` に格納
    }).execute()
    
    return jsonify(response.data), 201



def get_article_summaries():
    """
        DBにあるすべての記事のid, タイトル, 作成日, 要約を取得して返す
    """
    response = supabase.table("articles").select("id, title, timestamp, summary").execute()

    if not response.data or len(response.data) == 0:
        return jsonify({"error": "No articles found"}), 404
    
    return jsonify(response.data), 200  # 全要素をそのまま返す


def get_article(article_id):
    """
        指定された記事のidからid, タイトル, 記事の作成者, 作成日, 本文を取得して返す
    """
    response = supabase.table("articles").select("id, title, author, timestamp, content").eq("id", article_id).execute()
    # Supabase の response.data はリストで返るので、空かどうか確認
    if not response.data or len(response.data) == 0:
        return jsonify({"error": "Article not found"}), 404
    
    return jsonify(response.data[0]), 200  # 最初の要素（1つの辞書）を返す


def get_chat_history(chat_id):
    """
        DBからチャットの履歴を取得して返す関数
    """
    response = supabase.table("chats").select("chat").eq("id", chat_id).execute()

    if not response.data or len(response.data) == 0:
        return None

    chat_content = response.data[0].get("chat", "")

    return chat_content
