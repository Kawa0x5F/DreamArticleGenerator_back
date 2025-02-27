import os
from flask import jsonify
from google import genai
from chats.gemini_api_key import GEMINI_API_KEY
from supabase import create_client, Client
from dotenv import load_dotenv

# 仮書きのコード
prompt =   'あなたは夢についての記事の作成を補助する専門家です．\
            会話相手の夢についての情報を聞き出し，最終的にその夢についての記事を作成してください．\
            会話の内容を示します．いい感じになるように返答を生成してください．\
            また，返答は次の条件に沿って作成してください． \
            - 会話ではあなたが質問をします．質問は3つあります．\
                1. あなたの夢はなんですか？\
                2. その夢を持った理由はなんですか？\
                3. その夢で社会をどうしていきたいですか？\
            - 質問は会話相手がその質問に答えたと判断できたら次の質問に移ってください．\
            - 全ての質問が終わったら記事を作成します．\
            - 記事の作成条件は次のとおりです．\
                1. 記事は「タイトル」，「夢に関する詳細情報が書かれた本文」からなります．\
                2. 会話内容からわかることから適切に情報を付け足して本文を作成されます．\
                3. 記事の出力形式はMarkdownです．\
            以上です．よろしくお願いします．\
            '
load_dotenv()
SUPABASE_CHAT_URL = os.getenv("SUPABASE_CHAT_URL")
SUPABASE_CHAT_KEY = os.getenv("SUPABASE_CHAT_KEY")

supabase: Client = create_client(SUPABASE_CHAT_URL, SUPABASE_CHAT_KEY)

def create_new_chat():
    new_chat = {
        "chat": "user:\nこんにちは。あなたの夢はなんですか？\n"
    }
    response = supabase.table("chats").insert(new_chat).execute()

    # idを抽出
    id = response.data[0]['id']
    return jsonify({"id": id})

def join_message(user, past_chat, message):
    new_chat = past_chat + f'{user}:\n{message}\n'
    return new_chat

def generate_response(id, data):
    if "message" not in data:
        return "Bad request due to invalid input", 400

    supa_data = supabase.table("chats").select("*").eq("id", id).execute()
    past_chat = supa_data.data[0]['chat']
    message = data["message"]
    new_chat = join_message('user', past_chat, message)

    # Geminiのクライアントを作成する
    client = genai.Client(api_key=GEMINI_API_KEY)

    # チャットの返答を作成する
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt , new_chat]) #プロンプトと画像をgeminiに渡す

    # 生成された返答のテキストを抽出する
    response_message = response.text

    # 返答をテキストに結合する
    new_chat = join_message('gemini', new_chat, response_message)

    # 最新のチャット状況をDBに保存する
    new_chat = {
        "chat": new_chat
    }
    supabase.table("chats").update(new_chat).eq("id", id).execute()

    return response_message # 作成した応答を返す