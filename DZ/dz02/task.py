from flask import Flask, render_template, request, make_response, redirect, url_for, session

app = Flask(__name__)
app.secret_key = b'1a2a4f78926cb1a57ef2ee5cbcc6c6593c42c31c0e85b6ad782e248ff59b6dbc'


# Создать страницу, на которой будет форма для ввода имени
# и электронной почты
# При отправке которой будет создан cookie файл с данными
# пользователя
# Также будет произведено перенаправление на страницу
# приветствия, где будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка "Выйти"
# При нажатии на кнопку будет удален cookie файл с данными
# пользователя и произведено перенаправление на страницу
# ввода имени и электронной почты.


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        response = make_response(redirect(url_for("welcom", name=name)))
        response.set_cookie(name, email)
        return response
    return render_template("username_form.html")


@app.route('/welcom/<string:name>/', methods=['GET', 'POST'])
def welcom(name):
    return render_template("welcome_page.html", name=name)


@app.route('/logout/<string:name>/')
def logout(name):
    response = make_response(redirect(url_for("index")))
    response.set_cookie(name, max_age=0)
    return response


if __name__ == '__main__':
    app.run(debug=True)
