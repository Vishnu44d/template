import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from temp.config import DbEngine_config
from temp import create_db_engine, create_db_sessionFactory
from temp.models import createTables, destroyTables

from flask_cors import CORS
from dotenv import load_dotenv
from flask_cors import CORS

from temp.api import *

load_dotenv()

engine = create_db_engine(DbEngine_config)
SQLSession = create_db_sessionFactory(engine)

app = Flask(__name__)


CORS(app, supports_credentials=True)
@app.route('/')
def get():
    return "<h1> Hello, Welcome to backend </h1>"


app.register_blueprint(userBP, url_prefix='/user')



if __name__ == "__main__":
    app.run(debug=True)