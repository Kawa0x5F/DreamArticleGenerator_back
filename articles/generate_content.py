from articles.database import get_chat_history
from flask import Blueprint, request, jsonify
from google import genai
from config import Config

def run_generate_content(chat_history):
    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    content_prompt = """
    あなたは優秀な記事のライターです．次に示す会話から記事を生成してください。
    ただし，記事を生成する際は以下に示す条件を守ってください．\n
    - 記事の生成に利用するのは夢に関する会話の部分のみ
    - Markdonw形式で出力 
    - 出力時は記事の部分のみを出力してください
    - タイトルは別途記事から生成します．ので，タイトルは不要です．
    """
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[content_prompt , chat_history]) #プロンプトと会話履歴をgeminiに渡す
    response_content = response.text

    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    title_prompt = """
    次に夢について書かれた記事を示します．この記事のタイトルを生成してください．
    ただし，生成する際は次の条件に従ってください．
    - タイトルのみを出力
    - 最もテーマに合っていると考えられる1つのみを出力
    - 修飾なしの純粋な文字列のみで出力
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