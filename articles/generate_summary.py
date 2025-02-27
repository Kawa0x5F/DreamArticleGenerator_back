from google import genai
from config import Config

def content_to_summary(contents):

    # Geminiのクライアントを作成する
    client = genai.Client(api_key=Config.GEMINI_API_KEY)

    prompt = '次の記事の本文を要約してください．'

    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[prompt , contents]) #プロンプトと画像をgeminiに渡す

    response_summary = response.text

    return response_summary
