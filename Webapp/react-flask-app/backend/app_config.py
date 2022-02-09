import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'dataapi'),
    os.getenv('DB_PASSWORD', 'fnmwm4d833834erjn'),
    os.getenv('DB_HOST', 'dataapidb'),
    os.getenv('DB_NAME', 'dataapi')
)
db = SQLAlchemy(app)
ma = Marshmallow(app)





