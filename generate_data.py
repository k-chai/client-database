import sqlite3
from faker import Faker
import random
from transliterate import translit

# Создание соединения с базой данных clients.db
conn = sqlite3.connect('clients.db')
cursor = conn.cursor()

# Проверка и удаление таблиц, если они существуют
cursor.execute('DROP TABLE IF EXISTS Клиенты')
cursor.execute('DROP TABLE IF EXISTS Пользователи')

# Создание таблицы клиентов
cursor.execute('''
CREATE TABLE Клиенты (
    Номер_счета INTEGER PRIMARY KEY,
    Фамилия TEXT,
    Имя TEXT,
    Отчество TEXT,
    Дата_рождения DATE,
    ИНН CHAR(12),
    ФИО_ответственного TEXT,
    Статус TEXT DEFAULT 'Не в работе'
)
''')

# Создание таблицы пользователей
cursor.execute('''
CREATE TABLE Пользователи (
    ФИО TEXT,
    Логин VARCHAR(50),
    Пароль VARCHAR(50)
)
''')

# Использование Faker для генерации случайных данных
fake = Faker('ru_RU')


# Функция для генерации согласованного имени
def generate_name():
    gender = fake.random_element(elements=('male', 'female'))
    last_name = fake.last_name_male() if gender == 'male' else fake.last_name_female()
    first_name = fake.first_name_male() if gender == 'male' else fake.first_name_female()
    middle_name = fake.middle_name_male() if gender == 'male' else fake.middle_name_female()
    return last_name, first_name, middle_name


# Функция для генерации данных пользователей (ответственных лиц)
def generate_user_data(num_records):
    users = []
    for _ in range(num_records):
        full_name = ' '.join(generate_name())
        login = ''.join(filter(str.isalpha, translit(' '.join(full_name.split()[:2]), 'ru', reversed=True).lower()))
        password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        users.append((full_name, login, password))
    return users


# Функция для генерации случайных данных для клиентов
def generate_client_data(num_records, responsible_people):
    clients = []    
    for _ in range(num_records):
        account_number = _ + 1  # Номер счета идет по порядку, начиная с 1
        last_name, first_name, middle_name = generate_name()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
        inn = ''.join([str(fake.random_digit()) for _ in range(12)])
        responsible_person = random.choice(responsible_people)
        clients.append((account_number, last_name, first_name, middle_name, birth_date, inn, responsible_person))
    return clients


# Генерация данных пользователей
users = generate_user_data(50)

# Вставка данных в таблицу пользователей
cursor.executemany('''
INSERT INTO Пользователи (ФИО, Логин, Пароль)
VALUES (?, ?, ?)
''', users)

# Генерация и вставка данных в таблицу клиентов
clients = generate_client_data(500, [user[0] for user in users])
cursor.executemany('''
INSERT INTO Клиенты (Номер_счета, Фамилия, Имя, Отчество, Дата_рождения, ИНН, ФИО_ответственного)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', clients)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Данные успешно сгенерированы и добавлены в базу данных.")
