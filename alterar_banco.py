import sqlite3

# Conecta ao banco
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Tenta adicionar a coluna 'checkin'
try:
    c.execute("ALTER TABLE participantes ADD COLUMN checkin INTEGER DEFAULT 0;")
    print("✅ Coluna 'checkin' adicionada com sucesso.")
except sqlite3.OperationalError as e:
    print("⚠️ Erro: talvez a coluna já exista:", e)

conn.commit()
conn.close()
