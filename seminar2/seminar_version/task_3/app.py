from pathlib import PurePath, Path

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'

@app.context_processor
def menu_items():
    menu_items = [
        {'name': 'Home', 'url': url_for("index")},
        {'name': 'Task 1', 'url': url_for("task_1")},
        {'name': 'Task 2', 'url': url_for("task_2")},
        {'name': 'Task 3', 'url': url_for("task_3")}
    ]
    return dict(menu_items=menu_items)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/task_1', methods=['GET', 'POST'])
def task_1():
    if request.method == 'POST':
        return redirect(url_for('hello', name='User'))
    return render_template('task_1.html')


@app.route('/hello/<name>')
def hello(name):
    return f'Привет, {name}!'


@app.route('/task_2')
def task_2():
    return render_template('task_2.html')


@app.route('/task_2_upload', methods=['GET', 'POST'])
def task_2_upload():
    if request.method == 'POST':
        image = request.files.get('image')
        file_name = secure_filename(image.filename)
        Path(Path.cwd(), 'static', 'uploads').mkdir(exist_ok=True)
        image.save(
            PurePath.joinpath(Path.cwd(), 'static', 'uploads', file_name))
        return f"""Файл {file_name} загружен на сервер<br>
            <a href='{url_for('task_2_upload')}'>Назад</a>"""
    return render_template('form_task_2.html')


@app.route('/task_3', methods=['GET', 'POST'])
def task_3():
    login = 'l'
    password = 'p'
    if request.method == 'POST':
        l_r = request.form.get('login')
        p_r = request.form.get('password')
        if l_r == login and p_r == password:
            return redirect(url_for('hello', name=login))
        else:
            flash('Ошибка!, неверный логин или пароль', 'danger')
            return redirect(url_for('task_3'))
    return render_template('task_3.html')


if __name__ == '__main__':
    app.run(debug=True)
