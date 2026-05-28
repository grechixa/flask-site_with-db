import sqlite3

conn = sqlite3.connect('posts.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
''')

data = [
    ('Первый пост', 'Это мой первый блог-пост'),
    ('Flask это просто', 'Учимся Flask шаг за шагом'),
    ('Советы по Python', 'Полезные советы для новичков'),
]

# Проверяем, пустая ли таблица
cursor.execute('SELECT COUNT(*) FROM posts')
if cursor.fetchone()[0] == 0:
    cursor.executemany('''
        INSERT INTO posts (title, content)
        VALUES (?, ?)
    ''', data)

conn.commit()
conn.close()

print("✅ Таблица posts успешно создана и заполнена!")
