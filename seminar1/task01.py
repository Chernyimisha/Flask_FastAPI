from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'Здравствуй, Миша!'


@app.route('/about/')
def about():
    return 'about'


@app.route('/contact/')
def contact():
    return 'contact'


@app.route('/<int:num1>/<int:num2>/')
def sum_nums(num1, num2):
    return str(num1 + num2)


@app.route('/string/<string:line>/')
def lenth_line(line):
    return str(len(line))


@app.route('/world')
def world():
    return render_template('username_form.html')


@app.route('/students')
def students():
    head = {
        'name': 'Имя',
        'lastname': 'Фамилия',
        'age': 'Возраст',
        'rating': 'Средний бал'
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

    return render_template('username_form.html', **head, students=students)


if __name__ == '__main__':
    app.run(debug=True)
