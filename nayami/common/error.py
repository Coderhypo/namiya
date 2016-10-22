from flask import jsonify

from nayami.common.app import app


class Base(Exception):
    error_id = "BASE_ERROR"
    status_code = 500
    msg = "base error"

    def render(self):
        return dict(
            error_id=self.error_id,
            message=self.msg,
        )


class ValidationError(Base):
    error_id = "INVALID_ERROR"
    status_code = 400
    msg = "invalid args error"

    def __init__(self, msg=None):
        if msg:
            self.msg = msg


class NotFoundError(Base):
    error_id = "NOT_FOUND"
    status_code = 404
    msg = "resource not found"

    def __init__(self, msg=None):
        if msg:
            self.msg = msg


class NoPermission(Base):
    error_id = "NO_PERMISSION"
    status_code = 403
    msg = "wrong token"


@app.errorhandler(Base)
def handle_api_error(e):
    return jsonify(e.render()), e.status_code
