from flask import render_template, request, redirect, url_for
from app import app, get_db_connection
import sqlite3

#app = Flask(__name__)

@app.route("/students")
def students():
    conn = get_db_connection()
    students_data = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    
    # Преобразуем sqlite3.Row в словари
    students_list = [
        {
            "id": s["id"],
            "name": s["Имя"],
            "age": s["Возраст"],
            "grade": s["Оценка"],
            "status": s["Статус"]
        }
        for s in students_data
    ]
    
    threshold = 3
    return render_template("students.html", students=students_list, threshold=threshold)

@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        grade = request.form.get("grade", "").strip()
        
        if name and age and grade:
            try:
                age = int(age)
                grade = int(grade)
                
                # Определяем статус: если оценка >= 3, то "Сдал", иначе "Не сдал"
                status = "Сдал" if grade >= 3 else "Не сдал"
                
                conn = get_db_connection()
                conn.execute(
                    'INSERT INTO students ("Имя", "Возраст", "Оценка", "Статус") VALUES (?, ?, ?, ?)',
                    (name, age, grade, status)
                )
                conn.commit()
                conn.close()
                
                return redirect(url_for("students"))
            except ValueError:
                pass
    
    return render_template("add_student.html")


@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()

    if not student:
        return redirect(url_for('students'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        grade = request.form.get('grade', '').strip()

        if name and age and grade:
            try:
                age_i = int(age)
                grade_i = int(grade)
                status = 'Сдал' if grade_i >= 3 else 'Не сдал'

                conn = get_db_connection()
                conn.execute('UPDATE students SET "Имя" = ?, "Возраст" = ?, "Оценка" = ?, "Статус" = ? WHERE id = ?',
                             (name, age_i, grade_i, status, id))
                conn.commit()
                conn.close()
                return redirect(url_for('students'))
            except ValueError:
                pass

    # GET: показать форму с текущими данными
    student_data = {"id": student['id'], "name": student['Имя'], "age": student['Возраст'], "grade": student['Оценка']}
    return render_template('edit_student.html', student=student_data)


@app.route('/students/delete/<int:id>', methods=['POST'])
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('students'))

@app.route("/products")
def products():
    products_data = [
        {"name": "Телефон", "price": 500, "available": True},
        {"name": "Ноутбук", "price": 1200, "available": False},
        {"name": "Мышка", "price": 50, "available": True}
    ]
    threshold = 1000
    return render_template("products.html", products=products_data, threshold=threshold)

news_list = [
    {"title": "Новая технология ИИ", "views": 1500},
    {"title": "Открытие стартапа", "views": 800},
    {"title": "Обновление Python", "views": 2000},
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/news")
def news():
    return render_template("news.html", news=news_list)

@app.route("/posts")
def posts_list():
    try:
        conn = sqlite3.connect('posts.db')
        conn.row_factory = sqlite3.Row
        posts = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
        conn.close()
        posts_data = [{"id": p["id"], "title": p["title"], "content": p["content"]} for p in posts]
    except:
        posts_data = []
    
    return render_template("posts.html", posts=posts_data)

@app.route("/posts/<int:id>")
def post_detail(id):
    try:
        conn = sqlite3.connect('posts.db')
        conn.row_factory = sqlite3.Row
        post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
        conn.close()
        if post:
            post_data = {"id": post["id"], "title": post["title"], "content": post["content"]}
        else:
            post_data = None
    except:
        post_data = None
    
    return render_template("post_detail.html", post=post_data)

@app.route("/posts/add", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        
        if title and content:
            try:
                conn = sqlite3.connect('posts.db')
                conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
                conn.commit()
                conn.close()
                return redirect(url_for("posts_list"))
            except Exception as e:
                pass
    
    return render_template("add_post.html")

@app.route("/repos")
def repos():
    repos_list = [
        {"name": "Flask App", "language": "Python", "stars": 1500},
        {"name": "Frontend UI", "language": "JavaScript", "stars": 800},
        {"name": "Data Science", "language": "Python", "stars": 2300},
        {"name": "Simple Site", "language": "HTML", "stars": 300},
    ]

    threshold = 1000

    return render_template(
        "repos.html",
        repos=repos_list,
        threshold=threshold,
        total=len(repos_list)
    )

if __name__ == "__main__":
    app.run(debug=True)