from flask import Blueprint, request
from articles.database import add_article, get_article_summaries, get_article

article = Blueprint('article', __name__)

# 記事の追加
@article.route('/articles', methods=['POST'])
def create_article():
    return add_article(request.get_json())

# 全記事の要約取得
@article.route('/articles', methods=['GET'])
def fetch_summaries():
    return get_article_summaries()

# 記事本体の取得
@article.route('/article/<int:article_id>', methods=['GET'])
def fetch_full_article(article_id):
    return get_article(article_id)



