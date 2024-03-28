from flask import Flask
from flask import render_template

app1 = Flask(__name__)


@app1.route('/')
def hello_world():
    return 'Hello World!'


@app1.route('/Фёдор/')
@app1.route('/Fedor/')
@app1.route('/Федя/')
def fedor():
    """Функция представления имеет три декоратора. При переходе по любому из этих
    адресов в браузере отобразится одна и та же строка «Привет, Феодор!».
    """
    return 'Привет, Феодор!'


@app1.route('/')
@app1.route('/<name>/')
def hello(name='незнакомец'):
    """
    Функция будет отрабатывать корневой адрес и адреса, где передаётся любой текст
    между корневым слешем и замыкающим. При этом текст из браузера сохраняется в
    переменной <name>.
    Далее функция hello() принимает на вход содержимое переменной name. Если в
    браузере ничего не ввести, будет подставлено значение по умолчанию —
    «незнакомец».
    """
    return 'Привет, ' + name + '!'


"""Типы переменных при передаче в функцию
В примере выше мы передали через name строковое значение. Это действие по
умолчанию. Помимо этого можно передавать следующие данные:
● string — (по умолчанию) принимает текст без слеша
● int — принимает позитивные целые числа
● float — принимает позитивные числа с плавающей точкой
● path — как string, но принимает слэши
● uuid — принимает строки UUID
"""


@app1.route('/file/<path:file>/')
def set_path(file):
    """
    В примере ниже содержимое строки после file воспринимается как путь и попадает
    в переменную path независимо от количества слешей
    """
    print(type(file))
    return f'Путь до файла "{file}"'


@app1.route('/number/<float:num>/')
def set_number(num):
    """
    А в этом примере num ожидает число с плавающей запятой.
    Если вы попытаетесь передать данные другого типа, получим ошибку 404, страница
    не будет отработана.
    """
    print(type(num))
    return f'Передано число {num}'


html = """
    <h1>Привет, меня зовут Алексей</h1>
    <p>Уже много лет я создаю сайты на Flask.<br/>Посмотрите на мой сайт.</p>
    """


@app1.route('/text/')
def text():
    return html


@app1.route('/poems/')
def poems():
    poem = ['Вот не думал, не гадал,',
            'Программистом взял и стал.',
            'Хитрый знает он язык,',
            'Он к другому не привык.',
            ]
    txt = '<h1>Стихотворение</h1>\n<p>' + '<br/>'.join(poem) + '</p>'
    return txt


@app1.route('/index/<string:name>, <int:age>, <string:oldmather>')
def html_index(name: str, age: int, oldmather: str):
    return render_template('username_form.html', name=name, age=age, oldmather=oldmather)


@app1.route('/index2/')
def html_index2():
    context = {'name': 'Лиза', 'age': 4, 'oldmather': 'Таня'}
    return render_template('username_form.html', **context)


@app1.route('/poemsfor/')
def poems_for():
    context = {'poem': ['Вот не думал, не гадал,',
                        'Программистом взял и стал.',
                        'Хитрый знает он язык,',
                        'Он к другому не привык.',
                        ]}
    # txt = """<h1>Стихотворение</h1>\n<p>""" + '<br/>'.join(poem) + '</p>'
    return render_template('poems.html', **context)


@app1.route('/main/')
def main():
    return render_template('main.html')


@app1.route('/data/')
def data():
    return render_template('data.html')


if __name__ == '__main__':
    app1.run()
