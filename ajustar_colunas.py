import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

try:
    c.execute("ALTER TABLE participantes ADD COLUMN checkin_time TEXT;")
    print("✅ Coluna 'checkin_time' adicionada com sucesso.")
except sqlite3.OperationalError as e:
    print("⚠️ A coluna 'checkin_time' já existe ou erro:", e)

conn.commit()
conn.close()
