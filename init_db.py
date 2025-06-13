import sqlite3

def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS participantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                checkin INTEGER DEFAULT 0,
                checkin_time TEXT
            )
        ''')
        conn.commit()

if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado.")
