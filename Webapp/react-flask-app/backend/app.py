from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
import logger
from logic.test import test

log = logger.create_logger(__name__)
app = Flask(__name__)
log.info("Flask server started!")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'dataapi'),
    os.getenv('DB_PASSWORD', 'fnmwm4d833834erjn'),
    os.getenv('DB_HOST', 'dataapidb'),
    os.getenv('DB_NAME', 'dataapi')
)
db = SQLAlchemy(app)

test(db)


@app.route('/status')
def status():
    return 'Backend running!'


@app.route('/database')
def connection():
    if db is not None:
        status_message = "Database Connected!"
    else:
        status_message = "Database not Connected!"

    return status_message


if __name__ == '__main__':
    app.run(host='0.0.0.0')
