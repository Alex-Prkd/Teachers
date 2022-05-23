from flask_migrate import Migrate
from flask import Flask

from example.config import Config
from example.models import db
from example.forms import csrf

app = Flask(__name__)
csrf.init_app(app)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

from example.views import *


if __name__ == '__main__':
    app.run(debug=True)