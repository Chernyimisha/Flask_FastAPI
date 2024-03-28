from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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


@app.route('/task_1', methods=['GET', 'POST'])
def task_1():
    if request.method == 'POST':
        return redirect(url_for('hello', name='User'))
    return render_template('task_1.html')


@app.route('/hello/<name>')
def hello(name):
    return f'Привет, {name}!'


if __name__ == '__main__':
    app.run(debug=True)
