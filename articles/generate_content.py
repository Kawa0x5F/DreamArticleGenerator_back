from articles.database import get_chat_history
from flask import Blueprint, request, jsonify

def run_generate_content():
    pass


def generated_article(chat_id):
    chat_history = get_chat_history(chat_id)
    # title, content = run_generate_content(chat_history)
    title, content = "aa", f"{chat_history}"
    response = {
        "id" : chat_id,
        "title" : title,
        "content" : content
    }
    
    return jsonify(response), 200