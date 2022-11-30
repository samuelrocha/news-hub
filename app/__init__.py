from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

migrate = Migrate(app, db)

from app.controllers import default, module