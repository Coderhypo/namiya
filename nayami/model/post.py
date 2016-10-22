from flask import g
from uuid import uuid4
from datetime import datetime

from nayami.common.app import db
from nayami.config import RECIPIENT, SENDER


class Post(db.Model):
    id = db.Column('post_id', db.String(255), primary_key=True)

    content = db.Column(db.Text)
    recipient = db.Column(db.String(80))
    sender = db.Column(db.String(80))
    sender_email = db.Column(db.String(120), nullable=False)

    reply_id = db.Column("reply_id", db.String(255), index=True)

    create_time = db.Column(db.DateTime, default=datetime.now())
    distributed_time = db.Column(db.DateTime)
    replied_time = db.Column(db.DateTime)
    is_public = db.Column(db.Boolean)

    sender_ip = db.Column(db.String(80))
    sender_user_agent = db.Column(db.Text)

    def __init__(self):
        self.id = str(uuid4())
        self.create_time = datetime.now()
        self.distributed_time = datetime.now()
        self.reply_id = None
        self.replied_time = None
        self.is_public = False
        self.sender_ip = g.get("user_ip", "")
        self.sender_user_agent = str(g.get("user_agent", ""))

    @classmethod
    def get_post_by_id(cls, post_id):
        post = cls.query.filter_by(id=post_id).first()
        if not post:
            return None
        return post

    @classmethod
    def create_post(cls, sender, sender_email, content):
        post = cls()
        post.content = content
        post.recipient = RECIPIENT
        post.sender = sender
        post.sender_email = sender_email

        db.session.add(post)
        db.session.commit()
        return post

    def reply(self, sender_email, content):
        post = Post()
        post.content = content
        post.recipient = self.sender
        post.sender = SENDER
        post.sender_email = sender_email

        post.reply_id = self.id

        db.session.add(post)
        db.session.commit()
        return post

    @classmethod
    def get_unanswered_post(cls):
        post = cls.query.filter_by(replied_time=None, reply_id=None).order_by(cls.distributed_time).frist()
        post.distributed_time = datetime.now()
        db.session.add(post)
        db.session.commit()
        return post

    @classmethod
    def get_replies_by_post_id(cls, post_id):
        posts = cls.query.filter_by(reply_id=post_id).all()
        return posts

