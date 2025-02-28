"""
    チャットの履歴から記事の生成を行う
"""
from articles.database import get_chat_history
from flask import jsonify
from google import genai
from config import Config

def run_generate_content(chat_history):
    """
        チャットの履歴から記事の生成を行う
        生成した記事からタイトルの生成を行う
        生成したタイトルと記事を返す
    """

    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    content_prompt = """
    あなたは優秀な記事のライターです．次に示す会話から記事を生成してください。
    ただし，記事を生成する際は以下に示す条件を守ってください．\n
    - 記事の一人称のは会話で夢を語っている人
    - 記事の生成に利用するのは夢に関する会話の部分のみ
    - 会話で語られている夢に関連する知識を利用して情報量を増やす
    - Markdonw形式で出力
    - 出力時は記事の部分のみを出力
    - タイトルは不要
    - サブタイトルは任意で設定
    以上です．
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
    """
        生成した記事とタイトル,chat_idを応答として返す
    """

    chat_history = get_chat_history(chat_id)
    if chat_history is None:
        return jsonify({"error": "Generated article not found"}), 404
    content, title = run_generate_content(chat_history)
    response = {
        "id" : chat_id,
        "title" : title,
        "content" : content
    }
    return jsonify(response), 200