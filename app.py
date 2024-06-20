from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на случайную строку для безопасности

# Функция для установки соединения с базой данных
def get_db_connection():
    conn = sqlite3.connect('clients.db')
    conn.row_factory = sqlite3.Row
    return conn

# Страница авторизации
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Пользователи WHERE Логин = ? AND Пароль = ?', (login, password))
        user = cursor.fetchone()

        if user:
            session['logged_in'] = True
            session['username'] = user['ФИО']
            return redirect(url_for('clients'))
        else:
            return render_template('login.html', error='Неправильный логин или пароль.')

    return render_template('login.html', error=None)

# Страница с клиентами
@app.route('/clients', methods=['GET', 'POST'])
def clients():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    username = session['username']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Клиенты WHERE ФИО_ответственного = ?', (username,))
    clients = cursor.fetchall()

    if request.method == 'POST':
        account_numbers = request.form.getlist('account_number[]')
        new_statuses = request.form.getlist('new_status[]')

        if len(account_numbers) != len(new_statuses):
            return "Ошибка: количество номеров счетов не соответствует количеству статусов."

        for i in range(len(account_numbers)):
            account_number = account_numbers[i]
            new_status = new_statuses[i]

            # Получаем текущий статус клиента перед обновлением
            cursor.execute('SELECT Статус FROM Клиенты WHERE Номер_счета = ?', (account_number,))
            old_status = cursor.fetchone()['Статус']

            cursor.execute('UPDATE Клиенты SET Статус = ? WHERE Номер_счета = ?', (new_status, account_number))
            conn.commit()

            print(f"Изменение статуса клиента {account_number}: {old_status} -> {new_status}")

        return redirect(url_for('clients'))

    return render_template('clients.html', username=username, clients=clients)

# Выход из учетной записи
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
