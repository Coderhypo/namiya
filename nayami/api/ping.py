from flask import jsonify

from nayami.common.app import app
from nayami.config import VERSION


@app.route("/_ping")
def ping():
    return 'PONG'


@app.route('/_version')
def get_version():
    return jsonify(
        dict(version=VERSION)
    )
