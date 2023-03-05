from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import config
from config import IMG_FOLDER

app = Flask(__name__)
app.config.from_object(config)
CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
