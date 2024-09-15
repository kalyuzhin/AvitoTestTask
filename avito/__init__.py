from flask import Flask
from flask_migrate import Migrate
from .models import db
from .routes import main as main_blueprint

from os import environ

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = ('postgresql://cnrprod1725782375-team-77723:cnrprod1725782375-team-77723@rc1b'
                                  '-5xmqy6bq501kls4m.mdb.yandexcloud.net:6432/cnrprod1725782375-team-77723')  #
# environ.get('POSTGRES_CONN')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(main_blueprint)
with app.app_context():
    db.create_all()
