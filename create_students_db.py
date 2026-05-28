import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        "Имя" TEXT NOT NULL,
        "Возраст" INTEGER NOT NULL,
        "Оценка" INTEGER NOT NULL,
        "Статус" TEXT NOT NULL
    )
''')

data = [
    ('Иван', 20, 4, 'Сдал'),
    ('Анна', 22, 2, 'Не сдал'),
    ('Петр', 19, 3, 'Сдал')
]

cursor.executemany('''
    INSERT INTO students ("Имя", "Возраст", "Оценка", "Статус")
    VALUES (?, ?, ?, ?)
''', data)

conn.commit()
conn.close()

print("Таблица students успешно создана и заполнена!")
