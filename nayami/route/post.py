from flask import render_template

from nayami.common.app import app
from nayami.common.auth import user_auth


@app.route('/', methods=['GET'])
def index_page():
    return "hello world!"


@app.route('/p/<post_id>', methods=['GET'])
def get_post_page(post_id):
    pass


@app.route('/post', methods=['POST'])
@user_auth
def create_post_page():
    pass


@app.route('/<page_name>', methods=['GET'])
def other_page(page_name):
    pass

