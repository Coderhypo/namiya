# coding=utf-8
import os

# database config
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///../../mailbox.db")

# email config
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# default post RECIPIENT and reply SENDER name
RECIPIENT = u'浪矢先生'
SENDER = u'浪矢杂货店'

# other
TEST = bool(os.getenv("TEST", True))
API_TOKEN = os.getenv("API_TOKEN", "DANGEROUS")
VERSION = 'v0.1'
