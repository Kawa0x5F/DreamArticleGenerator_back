from google import genai
from chats.gemini_api_key import GEMINI_API_KEY

prompt = '以下に会話の内容を示します．いい感じになるように返答を生成してください．'
chat_history = ''

def get_text(data):
    text = data['text']
    return text

def join_text(text):
    global chat_history
    chat_history += text

def generate_response(data):
    global chat_history

    # 受け取ったjsonからチャットに当たるテキストデータを受け取る
    text = get_text(data)

    # テキストを結合する
    join_text(text)

    # Geminiのクライアントを作成する
    client = genai.Client(api_key=GEMINI_API_KEY)

    # チャットの返答を作成する
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt , chat_history]) #プロンプトと画像をgeminiに渡す

    # 生成された返答のテキストを抽出する

    res_text = response.text

    # 返答をテキストに結合する
    join_text(res_text)

    return res_text # 作成した応答を返す