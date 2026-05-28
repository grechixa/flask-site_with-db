from flask import Flask
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Импортируем маршруты из этого же пакета (app)
from app.routes import *