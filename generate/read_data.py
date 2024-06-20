import sqlite3

# Подключение к базе данных clients.db
conn = sqlite3.connect('clients.db')
cursor = conn.cursor()


# Функция для чтения данных из таблицы Клиенты
def read_clients():
    cursor.execute('SELECT * FROM Клиенты')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# Функция для чтения данных из таблицы Пользователи
def read_users():
    cursor.execute('SELECT * FROM Пользователи')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# Чтение данных из таблиц
print("Содержимое таблицы Клиенты:")
read_clients()

print("\nСодержимое таблицы Пользователи:")
read_users()

# Закрытие соединения с базой данных
conn.close()
