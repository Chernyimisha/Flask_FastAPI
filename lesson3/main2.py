from flask import Flask, render_template, request
from forms import LoginForm, RegistrationForm
from flask_wtf.csrf import CSRFProtect
from lesson3.forms import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = b'd170ba53a6694e420318fee6eaab1a49aee527acddc99cd3308e2fce8e896e01'
csrf = CSRFProtect(app)

# >>>import secrets
# >>>secrets.token_hex()


@app.route('/form', methods=['GET', 'POST'])
@csrf.exempt
def my_form():
    ...
    return "No CSRF protection!"


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        pass
    return render_template('login.html', form=form)

# В данном примере определен маршрут /login, который обрабатывает GET и POST
# запросы. В представлении создается объект LoginForm, который передается в
# шаблон login.html с помощью функции render_template. Если метод запроса POST и
# данные формы проходят валидацию, то выполняется обработка данных из формы.
# Шаблон login.html должен содержать тег form с указанием метода и адреса для
# отправки данных формы, а также поля формы с помощью тегов input.

# Внутри блока content определен тег form с методом POST и адресом /login. Для
# каждого поля формы вызывается соответствующий метод объекта формы
# (например, form.username для поля username) с указанием размера поля.


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        email = form.email.data
        password = form.password.data
        print(email, password)
        ...
    return render_template('register.html', form=form)

# В данном примере определен маршрут /register, который обрабатывает GET и POST
# запросы. В представлении создается объект RegistrationForm, который передается в
# шаблон register.html с помощью функции render_template. Если метод запроса POST
# и данные формы проходят валидацию, то выполняется обработка данных из формы.
# Данные из полей формы можно получить с помощью свойств data объекта формы.
# Например, для поля email можно получить значение следующим образом:
# form.email.data.

# В отличии от шаблона login.html мы не указываем поля явно. После стандартного
# вывода csrf токена создаём цикл для по всем полям формы за исключением токена.
# Для каждого поля выводится метка и окно поле ввода. Отдельно проверяем
# наличие ошибок ввода и если они есть, в цикле выводим все ошибки для каждого
# из полей. Таким образом мы динамически формируем страницу регистрации. А в
# случае неверного ввода данных пользователем, сразу сообщаем ему об ошибках.


if __name__ == '__main__':
    app.run(debug=True)

