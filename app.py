from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy 
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

app_context = app.app_context()
app_context.push()


logs_path = 'c:\logs\\'

os.makedirs(logs_path, exist_ok=True)
logging.basicConfig(level=logging.DEBUG,
                    handlers=[TimedRotatingFileHandler(logs_path + '/app.log', when='D', interval=1, backupCount=10)],
                    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                    datefmt='%Y-%m-%dT%H:%M:%S'
                    )
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    intro = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article%r>' % self.id

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create')
def create():
    return render_template('create.html')



if __name__ == '__main__':
    app.run(debug=True)