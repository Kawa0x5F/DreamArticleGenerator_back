from flask import Blueprint, request
from articles.database import add_article, get_article_title, get_article

article = Blueprint('article', __name__)

# 記事の追加
@article.route('/add', methods=['POST'])
def create_article():
    return add_article(request.get_json())


# タイトルのみ取得
@article.route('/fetch/title', methods=['GET'])
def fetch_title():
    return get_article_title({})

# タイトル、記事、ユーザーの取得
@article.route('/fetch/full', methods=['GET'])
def fetch_full_article():
    return get_article({})



