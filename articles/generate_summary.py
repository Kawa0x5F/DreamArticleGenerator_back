from google import genai
from config import Config

def content_to_summary(contents):

    # Geminiのクライアントを作成する
    client = genai.Client(api_key=Config.GEMINI_API_KEY)

    prompt = """
                次に自身の夢について書かれた記事を示します．
                以下の条件に従ってその記事の内容を要約してください．
                - 記事を書いた人の視点で要約する
                - 要約は50文字程度の長さに収める
                - 出力は要約分のみ
                以上です．よろしくお願いします．
             """

    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[prompt , contents]) #プロンプトと本文をgeminiに渡す

    response_summary = response.text

    return response_summary
