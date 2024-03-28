from flask import Flask
from flask import render_template
from datetime import datetime

app = Flask(__name__)


# Напишите простое веб-приложение на Flask, которое будет
# выводить на экран текст "Hello, World!".


@app.route('/')
def first_app():
    return "Hello, World!"

# Добавьте две дополнительные страницы в ваше вебприложение:
# ○ страницу "about"
# ○ страницу "contact".


@app.route('/about/')
def about():
    return render_template('base1.html')


@app.route('/contact/')
def contact():
    return render_template('base2.html')


# Написать функцию, которая будет принимать на вход два
# числа и выводить на экран их сумму.

@app.route('/summ/<int:number1>, <int:number2>/')
def summ(number1: int, number2: int):
    return str(number1 + number2)


# Написать функцию, которая будет принимать на вход строку и
# выводить на экран ее длину.

@app.route('/lenstr/<string:line>/')
def get_lenth(line: str):
    return str(len(line))


# Написать функцию, которая будет выводить на экран HTML
# страницу с заголовком "Моя первая HTML страница" и
# абзацем "Привет, мир!".

@app.route('/firstpage/')
def render_firstpage():
    return render_template('first_page.html')


# Написать функцию, которая будет выводить на экран HTML
# страницу с таблицей, содержащей информацию о студентах.
# Таблица должна содержать следующие поля: "Имя",
# "Фамилия", "Возраст", "Средний балл".
# Данные о студентах должны быть переданы в шаблон через
# контекст.

@app.route('/students/')
def get_students():

    attributes = {
        'name': 'Имя',
        'lastname': 'Фамилия',
        'age': 'Возраст',
        'rating': 'Средний балл',
    }

    students = [
        {'name': 'Миша',
         'lastname': 'Прошкин',
         'age': 39,
         'rating': 5},
        {'name': 'Алеша',
         'lastname': 'Иванов',
         'age': 18,
         'rating': 4},
        {'name': 'Игорь',
         'lastname': 'Андреев',
         'age': 25,
         'rating': 3}
    ]
    return render_template('students.html', **attributes, students=students)


# Написать функцию, которая будет выводить на экран HTML
# страницу с блоками новостей.
# Каждый блок должен содержать заголовок новости,
# краткое описание и дату публикации.
# Данные о новостях должны быть переданы в шаблон через
# контекст.

@app.route('/news/')
@app.route('/base/news/')
def get_news():
    attributes = {
        'name': 'Заголовок новости',
        'text': 'Краткое описание',
        'date': 'Дата публикации',
    }
    _news = [
        {
            "title": "John1",
            "descr": "Doe",
            "date": datetime.now().strftime("%H:%M - %m.%d.%y года"),
        },
        {
            "title": "John2",
            "descr": "Doe",
            "date": datetime.now().strftime("%H:%M - %m.%d.%y года"),
        },
        {
            "title": "John3",
            "descr": "Doe",
            "date": datetime.now().strftime("%H:%M - %m.%d.%y года"),
        },
    ]
    context = {'news': _news}
    return render_template('news.html', **context, **attributes)


# Создать базовый шаблон для всего сайта, содержащий
# общие элементы дизайна (шапка, меню, подвал), и
# дочерние шаблоны для каждой отдельной страницы.
# Например, создать страницу "О нас" и "Контакты",
# используя базовый шаблон.

@app.route('/basemain/')
def basemain():
    return render_template('basemain.html')


@app.route('/base/')
def base():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(debug=True)


