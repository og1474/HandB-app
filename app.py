from flask import Flask,render_template,request,redirect
import sqlite3,random
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
    answer_num = random.sample(range(0,9),4)
    answer = ''.join(str(n) for n in answer_num)

    if request.method == 'POST':
        enter = str(request.form['enter'])

    return render_template('index.html',
                           answer = answer)

if __name__ == '__main__':
    init_db()
    app.run(debug=True,port=5001)