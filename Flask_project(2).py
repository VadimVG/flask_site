from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
import sqlite3 as sq
from datetime import date

#Проект находится в стадии разработки
myapp = Flask(__name__)
myapp.config['SECRET_KEY']='GHJKJL;5091!gbnacvx'
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
            flash('Сообщение отправлено успешно', category='success') #названия категорий позволяют выбирать их в html документе и ссылаться на них в css для изменения стиля
        else:
            flash('Ошибка отправки сообщения', category='error')
    return render_template('feedback.html')


@myapp.route('/about') #О Нас
def about():
    return render_template('about.html')


@myapp.route('/login', methods=['GET', 'POST']) #воод логина и пароля
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'testname' and request.form['psw'] == '12qwe':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    else:
        return render_template('login.html')


@myapp.route('/profile/<username>') #профиль
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    else:
        return render_template('profile.html')


@myapp.route('/add_post', methods=['GET', 'POST']) #добавление постов
def addPost():
    if request.method == 'POST':
        if len(request.form['name'])>3 and len(request.form['post'])>5:
            base = sq.connect('myapp_base.db')
            cur = base.cursor()
            today = date.today()
            cur.execute('INSERT INTO add_post ("title", "text", "time") VALUES(?,?,?)', (request.form['name'], request.form['post'], today))
            base.commit()
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


if __name__=='__main__':
    myapp.run(debug=True)



















































































