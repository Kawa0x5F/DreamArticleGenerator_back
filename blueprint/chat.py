from flask import Blueprint, request
from chats.response import create_new_chat, generate_response

chat = Blueprint('chat', __name__)

# 新しくチャットを作成し，そのチャットのidを応答する
@chat.route('/get_id', methods=['GET'])
def get_id():
    return create_new_chat()

# 指定されたidのチャットの返答を応答する
@chat.route('/<int:id>', methods=['POST'])
def response(id):
    return generate_response(id, request.get_json())
