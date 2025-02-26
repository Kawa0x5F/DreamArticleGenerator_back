from google import genai
from chats.gemini_api_key import GEMINI_API_KEY

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
chat_history = 'あなた:\nこんにちは。あなたの夢はなんですか？\n'


def get_text(data):
    text = data['text']
    return text

def join_text(user, text):
    global chat_history
    chat_history += f'{user}:\n{text}\n'

    print(chat_history)

def generate_response(data):
    global chat_history

    # 受け取ったjsonからチャットに当たるテキストデータを受け取る
    text = get_text(data)

    # テキストを結合する
    join_text('あいて', text)

    # Geminiのクライアントを作成する
    client = genai.Client(api_key=GEMINI_API_KEY)

    # チャットの返答を作成する
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt , chat_history]) #プロンプトと画像をgeminiに渡す

    # 生成された返答のテキストを抽出する

    res_text = response.text

    # 返答をテキストに結合する
    join_text('あなた',res_text)

    return res_text # 作成した応答を返す