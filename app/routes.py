from flask import render_template
from app import app

#app = Flask(__name__)

@app.route("/students")
def students():
    students_data = [
        {"name": "Иван", "age": 20, "grade": 4},
        {"name": "Анна", "age": 22, "grade": 2},
        {"name": "Петр", "age": 19, "grade": 3}
    ]
    threshold = 3
    return render_template("students.html", students=students_data, threshold=threshold)

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

posts = [
    {"id": 1, "title": "Первый пост", "content": "Это мой первый блог-пост"},
    {"id": 2, "title": "Flask это просто", "content": "Учимся Flask шаг за шагом"},
    {"id": 3, "title": "Советы по Python", "content": "Полезные советы для новичков"},
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/news")
def news():
    return render_template("news.html", news=news_list)

@app.route("/posts")
def posts_list():
    return render_template("posts.html", posts=posts)

@app.route("/posts/<int:id>")
def post_detail(id):
    post = next((p for p in posts if p["id"] == id), None)
    return render_template("post_detail.html", post=post)

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