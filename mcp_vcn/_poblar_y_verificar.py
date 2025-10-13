import sqlite3
import os
from mcp.utilidades import crear_base_datos_si_no_existe

script = os.path.join(os.path.dirname(__file__), 'inicial.sql')
db = os.path.join(os.path.dirname(__file__), '..', 'vuelos.db')
db = os.path.abspath(db)

# Crear la base de datos si no existe
crear_base_datos_si_no_existe(db, script)

conn = sqlite3.connect(db)
c = conn.cursor()

c.execute('SELECT vuelo, COUNT(*) FROM reservas GROUP BY vuelo ORDER BY vuelo')
rows = c.fetchall()
print('Conteo de reservas por vuelo:')
for vuelo, cnt in rows:
    print(f'{vuelo}: {cnt}')

c.execute('SELECT COUNT(*) FROM reservas')
print('Total reservas:', c.fetchone()[0])

conn.close()
