from flask import g
from uuid import uuid4
from datetime import datetime
from markdown2 import markdown
from sqlalchemy import desc

from nayami.common.app import db
from nayami.config import RECIPIENT, SENDER


class Post(db.Model):
    id = db.Column('post_id', db.String(255), primary_key=True)

    content = db.Column(db.Text)
    content_md = db.Column(db.Text)
    content_len = db.Column(db.Integer)
    recipient = db.Column(db.String(80))
    sender = db.Column(db.String(80))
    sender_email = db.Column(db.String(120), nullable=False)

    reply_id = db.Column("reply_id", db.String(255), index=True)
    reply_email = db.Column("reply_email", db.String(120), index=True)
    from_namiya = db.Column(db.Boolean)
    is_read = db.Column(db.Boolean)

    create_time = db.Column(db.DateTime, default=datetime.now())
    last_post_time = db.Column(db.DateTime)
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
        self.reply_email = None
        self.is_read = False
        self.is_public = False
        self.from_namiya = False
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
        post.content_md = content
        post.content = markdown(content, extras=["fenced-code-blocks"], safe_mode=True)
        post.content_len = len(content)
        post.recipient = RECIPIENT
        post.sender = sender
        post.sender_email = sender_email

        db.session.add(post)
        db.session.commit()
        return post

    def reply(self, sender_email, content):
        post = Post()
        post.content_md = content
        post.content = markdown(content, extras=["fenced-code-blocks"], safe_mode=True)
        post.content_len = len(content)
        post.recipient = self.sender
        post.sender = SENDER
        post.sender_email = sender_email

        post.reply_id = self.id
        post.last_post_time = self.create_time
        post.reply_email = self.sender_email
        if not self.from_namiya:
            post.from_namiya = True
        db.session.add(post)

        self.replied_time = post.create_time
        db.session.add(self)
        db.session.commit()
        return post

    def read(self):
        self.is_read = True
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_rand_unanswered_post(cls):
        post = cls.query.filter_by(replied_time=None, from_namiya=False).order_by(cls.distributed_time).first()
        if not post:
            return None
        post.distributed_time = datetime.now()
        post.is_read = True
        db.session.add(post)
        db.session.commit()
        return post

    @classmethod
    def get_all_unanswered_post(cls):
        # mail box
        posts = cls.query.filter_by(replied_time=None, from_namiya=False).order_by(cls.create_time).all()
        return posts

    @classmethod
    def get_all_replies(cls):
        # milk box
        posts = cls.query.filter_by(from_namiya=True, is_read=False).order_by(desc(cls.create_time)).all()
        return posts

    @classmethod
    def get_replies_by_post_id(cls, post_id):
        posts = cls.query.filter_by(reply_id=post_id).all()
        return posts

    @classmethod
    def get_replies_by_email(cls, email):
        posts = cls.query.filter_by(reply_email=email).order_by(cls.create_time).all()
        return posts

