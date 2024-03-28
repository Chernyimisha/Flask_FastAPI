from flask import Flask, render_template, url_for
from models import db, Student
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///seminar3.db'
db.init_app(app)
migrate = Migrate(app, db)


@app.context_processor
def menu_items():
    menu_items = [
        {'name': 'Home', 'url': url_for("index")},
        {'name': 'Task 1', 'url': url_for("task_1")},
    ]
    return dict(menu_items=menu_items)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/task_1')
def task_1():
    all_students = Student.query.order_by(-Student.id).all()
    return render_template('task_1.html', students=all_students)
