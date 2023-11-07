from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
login_manager = LoginManager()

db = SQLAlchemy()

app = Flask(__name__)

UPLOAD_FOLDER = 'static/photos'
ALLOWED_EXTENSIONS = {'jpg','jpeg','png','gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manager.db'
app.secret_key = 'super mega secret key'

db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

import routes

if __name__ == '__main__':
    app.run(debug=True)