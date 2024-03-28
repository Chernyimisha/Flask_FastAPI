from flask import Flask, render_template, request, abort, redirect, url_for, flash
from pathlib import PurePath, Path
from werkzeug.utils import secure_filename
from markupsafe import escape

app = Flask(__name__)
app.secret_key = b'1a2a4f78926cb1a57ef2ee5cbcc6c6593c42c31c0e85b6ad782e248ff59b6dbc'

# Создать страницу, на которой будет кнопка "Нажми меня", при
# нажатии на которую будет переход на другую страницу с
# приветствием пользователя по имени.


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/task01/")
def task01():
    return render_template("task01.html")


# Создать страницу, на которой будет изображение и ссылка
# на другую страницу, на которой будет отображаться форма
# для загрузки изображений.


@app.route("/task02/")
def task02():
    return render_template("task02_1.html")


@app.route("/task02_2/", methods=['GET', 'POST'])
def task02_2():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'static', file_name))
        return f"Файл {escape(file_name)} загружен на сервер"
    return render_template("task02_2.html")


@app.route("/task03/", methods=['GET', 'POST'])
def task03():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if login == 'Misha' and password == 'Proshkin':
            return render_template("task03_1.html", login=login)
        else:
            return render_template("task03_2.html")
    return render_template("task03.html")


@app.route("/task04/", methods=['GET', 'POST'])
def task04():
    if request.method == 'POST':
        text = request.form.get('text')
        if text:
            number = len(text.split())
            return render_template("task04_1.html", number=number)
        else:
            return "Вы ничего не ввели. Попробуйте снова!"
    return render_template("task04.html")


@app.route("/task05/", methods=['GET', 'POST'])
def task05():
    if request.method == 'POST':
        num1 = int(request.form.get('num1'))
        num2 = int(request.form.get('num2'))
        operation = request.form.get('operation')
        number = 0
        if num1 and num2 and operation:
            if operation == '+':
                number = num1 + num2
            elif operation == '-':
                number = num1 - num2
            elif operation == '*':
                number = num1 * num2
            elif operation == '/':
                number = round(num1 / num2, 2)
            return render_template("task05_1.html", number=number)
        else:
            return "Вы не ввели один или несколько параметров. Попробуйте снова!"
    return render_template("task05.html")


@app.route("/task06/", methods=['GET', 'POST'])
def task06():
    if request.method == 'POST':
        name = request.form.get('name')
        age = int(request.form.get('age'))
        if name and age:
            if age >= 18:
                return render_template("task06_1.html", name=name)
            else:
                abort(404)
        else:
            return "Вы ничего не ввели. Попробуйте снова!"
    return render_template("task06.html")


@app.errorhandler(404)
def page_not_found(e):
    context = {
        'title': 'Доступ запрещен',
        'url': request.base_url,
    }
    return render_template('task06_2.html', **context), 404


@app.route("/task07/", methods=['GET', 'POST'])
def task07():
    if request.method == 'POST':
        number = request.form.get('number')
        if number:
            result = int(number) * int(number)
            return redirect(url_for("task07_1", num1=number, num2=result))
        else:
            return "Вы ничего не ввели. Попробуйте снова!"
    return render_template("task07.html")


@app.route("/task07_1/<int:num1>,<int:num2>")
def task07_1(num1, num2):
    return render_template("task07_1.html", number1=num1, number2=num2)


@app.route("/task08/", methods=['GET', 'POST'])
def task08():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            flash(f'Привет, {name}!', 'success')
        else:
            flash(f'Вы ничего не ввели. Попробуйте снова!!', 'danger')
        return redirect(url_for("task08_1"))
    return render_template("task08.html")


@app.route("/task08_1/")
def task08_1():
    return render_template("task08_1.html")


if __name__ == '__main__':
    app.run(debug=True)
