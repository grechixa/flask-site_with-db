import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('SELECT "Имя", "Возраст", "Оценка", "Статус" FROM students')
rows = cursor.fetchall()

print("Содержимое students.db:")
for row in rows:
    print(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}")

conn.close()



def create_student(name, age, grade, status):
    """Добавление нового студента"""
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO students ("Имя", "Возраст", "Оценка", "Статус")
        VALUES (?, ?, ?, ?)
    ''', (name, age, grade, status))
    
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()
    
    print(f"✅ Студент '{name}' добавлен с ID {student_id}")
    return student_id

# ========== READ (Чтение данных) ==========
def read_all_students():
    """Вывод всех студентов"""
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    
    print("\n" + "="*60)
    print(f"{'ID':<4} {'Имя':<15} {'Возраст':<8} {'Оценка':<8} {'Статус':<10}")
    print("="*60)
    
    for student in students:
        print(f"{student[0]:<4} {student[1]:<15} {student[2]:<8} {student[3]:<8} {student[4]:<10}")
    print("="*60 + "\n")
    
    return students

def read_student_by_id(student_id):
    """Поиск студента по ID"""
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    conn.close()
    
    if student:
        print(f"\n📘 Найден студент: ID={student[0]}, Имя={student[1]}, Возраст={student[2]}, Оценка={student[3]}, Статус={student[4]}\n")
        return student
    else:
        print(f"❌ Студент с ID {student_id} не найден\n")
        return None

def read_students_by_status(status):
    """Поиск студентов по статусу"""
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students WHERE "Статус" = ?', (status,))
    students = cursor.fetchall()
    conn.close()
    
    print(f"\n📚 Студенты со статусом '{status}':")
    for student in students:
        print(f"   - {student[1]} (ID={student[0]}, Оценка={student[3]})")
    print()
    
    return students

# ========== UPDATE (Обновление данных) ==========
def update_student(student_id, name=None, age=None, grade=None, status=None):
    """Обновление данных студента"""
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Получаем текущие данные студента
    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    current = cursor.fetchone()
    
    if not current:
        print(f"❌ Студент с ID {student_id} не найден")
        conn.close()
        return False
    
    # Используем новые значения или оставляем старые
    new_name = name if name else current[1]
    new_age = age if age else current[2]
    new_grade = grade if grade else current[3]
    new_status = status if status else current[4]
    
    cursor.execute('''
        UPDATE students 
        SET "Имя" = ?, "Возраст" = ?, "Оценка" = ?, "Статус" = ?
        WHERE id = ?
    ''', (new_name, new_age, new_grade, new_status, student_id))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Студент с ID {student_id} обновлён!")
    return True

# ========== DELETE (Удаление данных) ==========
def delete_student(student_id):
    """Удаление студента по ID"""
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Проверяем, существует ли студент
    cursor.execute('SELECT "Имя" FROM students WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    
    if not student:
        print(f"❌ Студент с ID {student_id} не найден")
        conn.close()
        return False
    
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()
    
    print(f"🗑️ Студент '{student[0]}' (ID={student_id}) удалён!")
    return True

def delete_all_students():
    """Удаление всех студентов (очистка таблицы)"""
    confirm = input("⚠️ Вы уверены, что хотите удалить ВСЕХ студентов? (да/нет): ")
    if confirm.lower() == 'да':
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students')
        conn.commit()
        conn.close()
        print("🗑️ Все студенты удалены!")
        return True
    else:
        print("❌ Операция отменена")
        return False
    
print(create_student("Коля", 20, 2, "не сдал"))