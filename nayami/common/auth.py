from flask import g, request
from functools import wraps

from nayami.config import API_TOKEN
from nayami.common.error import NoPermission


def user_auth(func):
    @wraps(func)
    def wrapper(*args, **kw):
        g.user_agent = request.user_agent
        g.user_ip = request.remote_addr
        return func(*args, **kw)

    return wrapper


def api_auth(func):
    @wraps(func)
    def wrapper(*args, **kw):
        token = request.headers.get("api_token")
        if token == API_TOKEN:
            return func(*args, **kw)
        raise NoPermission()

    return wrapper
