#!flask/bin/python
if __name__ == "__main__":
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=True)

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    handler = RotatingFileHandler(
        'deckbuilder.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
