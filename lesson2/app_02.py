from flask import Flask, url_for
from markupsafe import escape


app2 = Flask(__name__)


@app2.route('/')
def index():
    return 'Введи путь к файлу в адресной строке'


@app2.route('/<path:file>/')
def get_file(file):
    print(file)
    return f'Ваш файл находится в: {escape(file)}!'


@app2.route('/text_url_for/<int:num>/')
def text_url(num):
    text = f'В num лежит {num}<br>'
    text += f'Функция {url_for("text_url", num=42) = }<br>'
    text += f'Функция {url_for("text_url", num=42, data="new_data") = }<br>'
    text += f'Функция {url_for("text_url", num=42, data="new_data", pi=3.14515) = }<br>'
    return text


"""
При переходе по адресу test_url_for/7/ увидем следующий вывод:
В num лежит 7
Функция url_for("test_url", num=42) = '/test_url_for/42/'
Функция url_for("test_url", num=42, data="new_data") =
'/test_url_for/42/?data=new_data'
Функция url_for("test_url", num=42, data="new_data", pi=3.14515)
4
= '/test_url_for/42/?data=new_data&pi=3.14515'
Как видно из примера функция url_for принимает имя view функции в качестве
первого аргумента и любое количество ключевых аргументов. Каждый ключ
соответствует переменной в URL адресе. Отсутствующие в адресе переменные
добавляются к адресу в качестве параметров запроса, т.е. после знака вопрос “?”
как пары ключ-значение, разделённые символом &.
"""


@app2.route('/get/')
def get():
    if level := request.args.get('level'):
        text = f'Похоже ты опытный игрок, раз имеешь уровень {level}<br>'
    else:
        text = 'Привет, новичок.<br>'
    return text + f'{request.args}'


"""
В первую очередь мы импортировали request — глобальный объект Flask, который
даёт доступ к локальной информации для каждого контекста запроса. Звучит
сложно. Если проще, то request содержит данные, которую клиент передаёт на
сторону сервера.
Дополнительные параметры собираются в словаре args объекта request. И раз
перед нами словарь, можно получить значение обратившись к ключу через метод
get().
Перейдём по адресу http://127.0.0.1:5000/get/?name=alex&age=13&level=80 и
увидим следующий вывод:
Похоже ты опытный игрок, раз имеешь уровень 80
7
ImmutableMultiDict([('name', 'alex'), ('age', '13'), ('level',
'80')])
"""


if __name__ == '__main__':
    app2.run()