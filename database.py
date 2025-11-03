import sqlite3

def crear_tabla():
    conn = sqlite3.connect("turnos.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente TEXT NOT NULL,
            especialidad TEXT NOT NULL,
            medico TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            estado TEXT DEFAULT 'confirmado'
        )
    ''')
    conn.commit()
    conn.close()


def agregar_turno(paciente, especialidad, medico, fecha, hora):
    conn = sqlite3.connect("turnos.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO turnos (paciente, especialidad, medico, fecha, hora)
        VALUES (?, ?, ?, ?, ?)
    ''', (paciente, especialidad, medico, fecha, hora))
    conn.commit()
    conn.close()


def obtener_turnos():
    conn = sqlite3.connect("turnos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM turnos")
    turnos = cursor.fetchall()
    conn.close()
    return turnos


def cancelar_turno(id_turno):
    conn = sqlite3.connect("turnos.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE turnos SET estado = 'cancelado' WHERE id = ?", (id_turno,))
    conn.commit()
    conn.close()
