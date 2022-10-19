import sqlite3 as sq


base=sq.connect('myapp_base.db')#создание бд, если ее нет, или подключение, если она есть
cur=base.cursor()# с помощью данного класса вносятся изменения/происходит чтение даных из бд

base.execute("""CREATE TABLE IF NOT EXISTS add_post(
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    text text NOT NULL,
    time INTEGER NOT NULL
    );""") #создание таблицы
base.commit()

base.execute("""CREATE TABLE IF NOT EXISTS feedback(
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email text NOT NULL,
    message text NOT NULL,
    time INTEGER NOT NULL
    );""")
base.commit()

base.execute("""CREATE TABLE IF NOT EXISTS users(
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    time INTEGER NOT NULL
    );""")
base.commit()

#cur.execute('SELECT name FROM sqlite_master') #запрос на получение всех таблиц из базы
#res=cur.fetchall() #получение выборки
#print(res)


cur.execute(f"SELECT * FROM users")
res = cur.fetchall()
print(res)
if base.close:
    print('БД закрыта')
else:
    print('Ошибка при закрытии БД')
























































