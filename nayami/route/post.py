from flask import render_template, request, abort, redirect, url_for
from datetime import datetime

from nayami.common.app import app
from nayami.common.auth import user_auth
from nayami.model.post import Post


@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')


@app.route('/p/<post_id>', methods=['GET', 'POST'])
def get_post_page(post_id):
    if request.method == 'GET':
        return render_template('post/need_email.html', post_id=post_id)

    email = request.form.get("email")
    post = Post.get_post_by_id(post_id)
    if not post or post.reply_email != email:
        recipient = post.recipient if post else u'John Winston Lennon'
        return render_template('post/need_email.html', post_id=post_id, recipient=recipient)
    post.read()
    return render_template('post/post.html', post=post)


@app.route('/post', methods=['GET', 'POST'])
@user_auth
def create_post_page():
    if request.method == 'GET':
        return render_template('post/create_post.html')
    if request.method == 'POST':
        content = request.form.get("content")
        sender = request.form.get("sender")
        sender_email = request.form.get("sender_email")
        post = Post.create_post(sender, sender_email, content)
        assert post.id
        return redirect(url_for("mail_box_page"))


@app.route('/mailbox', methods=['GET'])
@user_auth
def mail_box_page():
    posts = Post.get_all_unanswered_post()
    return render_template('mailbox.html', posts=posts)


@app.route('/milkbox', methods=['GET'])
@user_auth
def milk_box_page():
    posts = Post.get_all_replies()
    return render_template('milkbox/list.html', posts=posts)


@app.route('/backdoor', methods=['GET', 'POST'])
@user_auth
def back_door_page():
    now = datetime.now().hour
    from nayami.config import TEST
    if TEST and (now > 8 or now < 22):
        return render_template('backdoor/help.html')

    if request.method == 'GET':
        need = request.args.get('need')
        if need == 'true':
            post = Post.get_rand_unanswered_post()
            if post:
                return render_template('backdoor/reply_post.html', post=post)
        post_id = request.args.get("p")
        post = Post.get_post_by_id(post_id) if post_id else None
        if post and not post.from_namiya:
            post.read()
            return render_template('backdoor/reply_post.html', post=post)
        posts = Post.get_all_unanswered_post()
        return render_template('backdoor/list.html', posts=posts)
    if request.method == 'POST':
        post_id = request.form.get("post_id")
        content = request.form.get("content")
        sender_email = request.form.get("sender_email")
        post = Post.get_post_by_id(post_id)
        if post:
            post.reply(sender_email, content)
        return redirect(url_for("back_door_page"))


@app.route('/<page_name>', methods=['GET'])
def other_page(page_name):
    if page_name in ['help']:
        return render_template('page/%s.html' % page_name)
    abort(404)
