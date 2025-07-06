from flask import Flask,render_template,request,redirect,session
import sqlite3,random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'answer_secret_key'

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT,
            hit INTEGER,
            blow INTEGER          
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/",methods=['GET','POST'])
def index():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    if 'answer' not in session:
        answer_num = random.sample(range(0,10),4)
        session['answer'] = ''.join(str(n) for n in answer_num)

    answer = session['answer']

    if request.method == 'POST':
        action = request.form.get('action') ##valueの値を取得

        if action == 'check':
            enter = str(request.form['enter'])
            hit = 0
            blow = 0
            for i in range(4):
                for j in range(4):
                    if enter[i] == answer[j]:
                        if i == j:
                            hit += 1
                        else:
                            blow += 1
            c.execute('INSERT INTO data (number,hit,blow) VALUES(?,?,?)',(enter,hit,blow)) ##テーブルに保存
            conn.commit()
    
        if action == 'new':
            answer_num = random.sample(range(0,10),4)
            session['answer'] = ''.join(str(n) for n in answer_num)
            c.execute('DELETE FROM data')
            conn.commit()

    answer = session['answer']
    c.execute('SELECT number,hit,blow FROM data') ##データベースから記録を取得
    data = c.fetchall()
    conn.close()
    return render_template('index.html',
                           answer = answer,
                           data = data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True,port=5001)