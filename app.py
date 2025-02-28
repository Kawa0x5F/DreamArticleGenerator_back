"""
    Flaskのappを作成し,Flaskを起動する
"""
from flask import Flask
from flask_cors import CORS

def create_app():
    """
        Flaskのappを作成して返す
    """
    app = Flask(__name__)

    # CORSエラーが発生しないようにするための設定
    CORS(app, supports_credentials=True)

    # Blueprintの登録
    from blueprint import article, chat
    app.register_blueprint(article.article, url_prefix="/api")
    app.register_blueprint(chat.chat, url_prefix="/api/chat")

    return app

if __name__ == '__main__':
    app = create_app()
    port = 5000
    app.run(host="0.0.0.0", port=port, debug=True)