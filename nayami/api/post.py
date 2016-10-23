from flask import request, jsonify

from nayami.common.app import app
from nayami.common.auth import user_auth, api_auth
from nayami.common.error import NotFoundError
from nayami.common.schema import PostSchema, ReplySchema

from nayami.model.post import Post


@app.route('/api/posts', methods=['POST'])
@user_auth
@api_auth
def create_post():
    schema = PostSchema()
    data = schema.to_dict(request.get_json())
    post = Post.create_post(sender=data['sender'],
                            sender_email=data['sender_email'],
                            content=data['content'])

    return jsonify(schema.dump(post).data)


@app.route('/api/posts/<post_id>', methods=['GET'])
@user_auth
@api_auth
def get_post(post_id):
    post = Post.get_post_by_id(post_id)
    if not post:
        raise NotFoundError()
    schema = PostSchema()
    return jsonify(schema.dump(post).data)


@app.route('/api/posts/<post_id>', methods=['POST'])
@user_auth
@api_auth
def reply_post(post_id):
    post = Post.get_post_by_id(post_id)
    if not post:
        raise NotFoundError()

    p_schema = PostSchema()
    r_schema = ReplySchema()
    data = r_schema.to_dict(request.get_json())
    reply = post.reply(sender_email=data['sender_email'],
                       content=data['content'])

    from nayami.util.email import MailSender
    sender = MailSender(reply.reply_email)
    sender.set_message_by_post(reply)
    sender.send()

    return jsonify(p_schema.dump(reply).data)

