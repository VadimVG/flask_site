from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
import sqlite3 as sq
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

#Проект находится в стадии разработки
myapp = Flask(__name__)
myapp.config['SECRET_KEY']='jdflAS89121)(*1HJL'
@myapp.errorhandler(404) #декоратор, позволяющий обрабатывать ошибки
def pagenotfound(error):
    return render_template('error_page404.html'), 404


@myapp.route('/') #главная станица
def index():
    base = sq.connect('myapp_base.db')  # создание бд, если ее нет, или подключение, если она есть
    cur = base.cursor()  # изменение/чтение даных из бд
    cur.execute(f'SELECT * FROM add_post ORDER BY time DESC')  # запрос на получение данных из таблицы
    res = cur.fetchall()  # получение выборки в переменную
    return render_template("index.html", title=res)


@myapp.route('/feedback', methods=['GET', 'POST']) #обратная связь
def feedback():
    if request.method == 'POST':
        if len(request.form['username']) > 2 and '@' in request.form['email']:
            base = sq.connect('myapp_base.db')
            cur = base.cursor()
            today = date.today()
            cur.execute('INSERT INTO feedback ("name", "email", "message", "time") VALUES(?,?,?,?)', (request.form['username'], request.form['email'], request.form['message'], today))  # запись в бд
            base.commit()  # сохранение изменений в бд
            base.close()
            flash('Сообщение отправлено успешно', category='success') #названия категорий позволяют выбирать их в html документе и ссылаться на них в css для изменения стиля
        else:
            flash('Ошибка отправки сообщения', category='error')
    return render_template('feedback.html')


@myapp.route('/about') #О Нас
def about():
    return render_template('about.html')


@myapp.route('/registration', methods=['POST', 'GET']) #регистрация пользователя, хэширование пароля
def reg():
    if request.method == 'POST':
        base_rep = sq.connect('myapp_base.db')
        cur_rep = base_rep.cursor()
        cur_rep.execute(f"SELECT COUNT() AS `count` FROM users WHERE email LIKE '{request.form['email']}'")
        rep=cur_rep.fetchall()
        base_rep.close()
        if 0 in rep[0]:
            if len(request.form['username'])>5 and len(request.form['email'])>5 and '@' in request.form['email'] and len(request.form['psw'])>5 and request.form['psw']==request.form['psw_1']:
                hash = generate_password_hash(request.form['psw'])
                today = date.today()
                base = sq.connect('myapp_base.db')
                cur = base.cursor()
                res=cur.execute('INSERT INTO users ("name", "email", "password", "time") VALUES(?,?,?,?)', (request.form['username'], request.form['email'], hash, today))  # запись в бд
                base.commit()  # сохранение изменений в бд
                base.close()
                if res:
                    flash("Вы успешно зарегистрированы", category='success')
                    return render_template('registration.html')
                else:
                    flash("Ошибка добавления данных в БД", category='error')
                    return render_template('registration.html')
            else:
                flash("Некорректно заполнены поля", category='error')
                return render_template('registration.html')
        else:
            flash('Пользователь с таким email-ом уже существует', category='error')
            return render_template('registration.html')
    else:
        return render_template('registration.html')


@myapp.route('/login', methods=['GET', 'POST']) #ввод логина и пароля
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'testname' and request.form['psw'] == '12qwe':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    else:
        return render_template('login.html')


@myapp.route('/add_post', methods=['GET', 'POST']) #добавление постов
def addPost():
    if request.method == 'POST':
        if len(request.form['name'])>3 and len(request.form['post'])>5:
            base = sq.connect('myapp_base.db')
            cur = base.cursor()
            today = date.today()
            cur.execute('INSERT INTO add_post ("title", "text", "time") VALUES(?,?,?)', (request.form['name'], request.form['post'], today))
            base.commit()
            base.close()
            flash('Статья добавлена успешно', category='success')
            return render_template('addPost.html')
        else:
            flash('Ошибка добавления статьи', category='error')
            return render_template('addPost.html')
    else:
        return render_template('addPost.html')


@myapp.route('/post/<int:id>')#публикация добавленных постов на главной странице
def post(id):
    base = sq.connect('myapp_base.db')
    cur = base.cursor()
    cur.execute(f'SELECT * FROM add_post WHERE _id={id}')
    res = cur.fetchall()
    return render_template('post.html', title=res)


@myapp.route('/post/<int:id>/del') #удаление постов
def del_post(id):
    base = sq.connect('myapp_base.db')
    cur = base.cursor()
    try:
        cur.execute(f'DELETE FROM add_post WHERE _id={id}')
        base.commit()
        return redirect('/')
    except:
        print('При удалении произошла ошибка')


#if __name__=='__main__':
    #myapp.run(debug=True)



















































































