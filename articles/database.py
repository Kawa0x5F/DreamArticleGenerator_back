from flask import Blueprint, request, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import supabase
from datetime import datetime, timezone, timedelta
from config import Config
from articles.generate_summary import content_to_summary

supabase: Client = create_client(
    Config.SUPABASE_ARTICUL_URL, Config.SUPABASE_ARTICUL_KEY
    )

# 記事の追加
def add_article(data):
    title = data.get("title")
    content = data.get("content")  
    summary = content_to_summary(content)
    author = data.get("author")  
    timestamp = datetime.now(timezone(timedelta(hours=9))).strftime("%Y年%m月%d日")

    if not title or not content or not author:
        return jsonify({"error": "title, content, author are required"}), 400
    
    response = supabase.table("articles").insert({
        "title": title,
        "content": content,
        "summary": summary,
        "author": author,
        "timestamp": timestamp
    }).execute()
    
    return jsonify(response.data), 201



def get_article_summaries():
    response = supabase.table("articles").select("id, title, timestamp, summary").execute()

    if not response.data or len(response.data) == 0:
        return jsonify({"error": "No articles found"}), 404
    
    return jsonify(response.data), 200  # 全要素をそのまま返す


def get_article(article_id):
    response = supabase.table("articles").select("id, title, author, timestamp, content").eq("id", article_id).execute()
    # Supabase の response.data はリストで返るので、空かどうか確認
    if not response.data or len(response.data) == 0:
        return jsonify({"error": "Article not found"}), 404
    
    return jsonify(response.data[0]), 200  # 最初の要素（1つの辞書）を返す


def get_chat_history(chat_id):
    response = supabase.table("chats").select("chat").eq("id", chat_id).execute()

    if not response.data or len(response.data) == 0:
        return None

    chat_content = response.data[0].get("chat", "")

    return chat_content
