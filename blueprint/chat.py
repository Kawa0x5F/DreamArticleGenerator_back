from flask import Blueprint, request
from chats.response import generate_response

chat = Blueprint('chat', __name__)
@chat.route('/')
def index():
    return generate_response(request.get_json())
