from articles.database import get_chat_history
from flask import Blueprint, request, jsonify
from google import genai
from config import Config

def run_generate_content(chat_history):
    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    content_prompt = """
    この会話から記事を生成してください。
    ただし、記事にする部分は、夢に関する会話だけを利用するようにしてください。
    """
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[content_prompt , chat_history]) #プロンプトと会話履歴をgeminiに渡す
    response_content = response.text

    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    title_prompt = """
    この記事のタイトルを生成してください。
    """
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[title_prompt , response_content]) #プロンプトと記事本体をgeminiに渡す
    response_title = response.text

    return  response_content, response_title


def generated_article(chat_id):
    chat_history = get_chat_history(chat_id)
    content, title = run_generate_content(chat_history)
    # title = "aa"
    # title, content = "aa", f"{chat_history}"
    response = {
        "id" : chat_id,
        "title" : title,
        "content" : content
    }
    
    return jsonify(response), 200