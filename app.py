from flask import Flask,render_template,request,redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            hit REAL,
            blow REAL          
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/",methods=['GET','POST'])
def index():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    if request.method == 'POST':
        number = str(request.form['enter'])