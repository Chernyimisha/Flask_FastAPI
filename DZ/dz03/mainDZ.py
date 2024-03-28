from flask import Flask, render_template, request, flash
from flask_wtf.csrf import CSRFProtect
from DZ.dz03.formsWTF import RegisterForm
from DZ.dz03.modelsDB import db, User
from cryptography.fernet import Fernet

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
app.config['SECRET_KEY'] = b'd170ba53a6694e420318fee6eaab1a49aee527acddc99cd3308e2fce8e896e01'
csrf = CSRFProtect(app)

# Генерация ключа
key = Fernet.generate_key()
cipher_suite = Fernet(key)


# Создать форму для регистрации пользователей на сайте.
# Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
# При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/reg/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate():
            name = form.name.data
            surname = form.surname.data
            email = form.email.data
            password = bytes(form.password.data, 'utf-8')
            encrypted_pass = cipher_suite.encrypt(password)
            user = User(username=name, usersurname=surname, email=email, password=encrypted_pass)
            db.session.add(user)
            db.session.commit()
            flash('Successfully registered')

    return render_template('register.html', form=form)




if __name__ == '__main__':
    app.run(debug=True)