import utilities.gutenberg
import gutencloud.orm
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    path.join('..', 'local_data', 'gutenberg.db')
db = SQLAlchemy(app)




