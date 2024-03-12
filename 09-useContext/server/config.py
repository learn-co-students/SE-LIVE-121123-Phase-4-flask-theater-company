# 1.✅ Import Bcrypt form flask_bcrypt
# 1.1 Invoke Bcrypt and pass it app
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

app.secret_key = b"@~xH\xf2\x10k\x07hp\x85\xa6N\xde\xd4\xcd"

db = SQLAlchemy(engine_options={"echo": True})
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

db.init_app(app)

Api.error_router = lambda self, handler, e: handler(e)
api = Api(app)
