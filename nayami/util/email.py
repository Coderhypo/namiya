# coding=utf-8
from flask_mail import Mail
from flask_mail import Message
import urlparse

from nayami.common.app import app
from nayami.config import EMAIL_SENDER, SMTP_SERVER, EMAIL_PASSWORD, TEST, SERVER_URL


app.config['MAIL_SERVER'] = SMTP_SERVER
app.config['MAIL_USERNAME'] = EMAIL_SENDER
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_PORT'] = 465
app.config['MAIL_DEBUG'] = TEST

mail = Mail()
mail.init_app(app)


class MailSender(object):
    sender = EMAIL_SENDER
    subject = u'[浪矢杂货]你有新的回复, 请注意查收'
    content = ""

    def __init__(self, recipient, subject=None):
        if subject:
            self.subject = subject
        self.recipient = recipient

    def set_message_by_post(self, post):
        template = u"""
        <p>%s, 你好</p>
        <p>在浪矢杂货店有关于你的新回复, 请注意查收<p>
        <p>请点击下面的连接: </p>
        <p><a href="%s">%s</a></p>
        """
        path = urlparse.urljoin(SERVER_URL, 'p/%s' % post.id)
        self.content = template % (post.recipient, path, path)

    def send(self):
        msg = Message(self.subject,
                      sender=(u'浪矢杂货店', self.sender),
                      recipients=[self.recipient])
        msg.html = self.content
        try:
            mail.send(msg)
        except Exception as e:
            print e
            pass


