from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # CORSの設定
    CORS(app)

    from blueprint import article, chat
    app.register_blueprint(article.article, url_prefix="/api")
    app.register_blueprint(chat.chat, url_prefix="/api/chat")

    return app

if __name__ == '__main__':
    app = create_app()
    port = 5000
    app.run(host="0.0.0.0", port=port, debug=True)