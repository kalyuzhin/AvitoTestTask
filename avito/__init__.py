from flask import Flask
from flask_migrate import Migrate
from .models import db
from .routes import main as main_blueprint

from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('POSTGRES_CONN')
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(main_blueprint)
with app.app_context():
    db.create_all()
