from flask import Blueprint

chat = Blueprint('chat', __name__)
@chat.route('/')
def index():
    return 'chat'
