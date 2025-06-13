from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
from flask_session import Session
import sqlite3
import qrcode
import os
import csv
import io
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_senha_secreta'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Cria banco se não existir
def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS participantes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT NOT NULL,
                        checkin INTEGER DEFAULT 0,
                        checkin_time TEXT
                    )''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']

        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO participantes (nome, email) VALUES (?, ?)", (nome, email))
            user_id = c.lastrowid
            conn.commit()

        # Gera QR Code com o ID do participante
        qr = qrcode.make(str(user_id))
        img_path = f'static/qr_codes/qr_{user_id}.png'
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        qr.save(img_path)

        return render_template('qr_code.html', user_id=user_id, img_path=img_path)
    return render_template('register.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/checkin/<int:user_id>', methods=['POST'])
def checkin(user_id):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("UPDATE participantes SET checkin = 1, checkin_time = ? WHERE id = ?", (datetime.now().isoformat(), user_id))
        conn.commit()
    return 'Check-in realizado com sucesso!'

@app.route('/verify_id', methods=['POST'])
def verify_id():
    user_id = request.json.get('id')
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM participantes WHERE id = ?", (user_id,))
        participante = c.fetchone()

        if participante:
            if participante[3] == 1:
                return jsonify({'status': 'info', 'message': 'Check-in já realizado!'})
            c.execute("UPDATE participantes SET checkin = 1, checkin_time = ? WHERE id = ?", (datetime.now().isoformat(), user_id))
            conn.commit()
            return jsonify({'status': 'success', 'nome': participante[1]})
        else:
            return jsonify({'status': 'error', 'message': 'ID não encontrado'})

@app.route('/dashboard')
def dashboard():
    if not session.get('logado'):
        return redirect(url_for('login'))
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("SELECT id, nome, email, checkin, checkin_time FROM participantes")
        participantes = c.fetchall()
    return render_template('dashboard.html', participantes=participantes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form['senha']
        if senha == 'admin123':
            session['logado'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', erro='Senha incorreta')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('index'))

@app.route('/export')
def export():
    if not session.get('logado'):
        return redirect(url_for('login'))

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Nome', 'Email', 'Check-in', 'Check-in Time'])

    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute("SELECT id, nome, email, checkin, checkin_time FROM participantes")
        for row in c.fetchall():
            writer.writerow(row)

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='participantes.csv'
    )

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
