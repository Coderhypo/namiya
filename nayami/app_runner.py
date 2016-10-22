from config import TEST
from nayami.common.app import app, db

try:
    db.create_all()
except Exception:
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=TEST)

