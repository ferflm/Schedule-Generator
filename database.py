import sqlite3

conn = sqlite3.connect("schedule.db")

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS options (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        professor_name TEXT NOT NULL,
        "group" TEXT NOT NULL,
        days TEXT NOT NULL,
        time TEXT NOT NULL,
        preference INTEGER DEFAULT 0,
        FOREIGN KEY (subject_id) REFERENCES subjects (id)
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        rank INTEGER NOT NULL,
        schedule JSON NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions (id)
    );
''')

conn.commit()
conn.close()

# Función para obtener todas las materias
def get_all_subjects():
    conn = sqlite3.connect("school_schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()
    conn.close()
    return subjects

# Función para obtener todas las opciones de una materia específica
def get_options_by_subject(subject_id):
    conn = sqlite3.connect("school_schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM options WHERE subject_id = ?", (subject_id,))
    options = cursor.fetchall()
    conn.close()
    return options

# Función para agregar una nueva materia
def add_subject(name):
    conn = sqlite3.connect("school_schedule.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

# Función para agregar una nueva opción de materia
def add_option(subject_id, professor_name, group, days, time, preference):
    conn = sqlite3.connect("school_schedule.db")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO options (subject_id, professor_name, "group", days, time, preference)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (subject_id, professor_name, group, days, time, preference))
    conn.commit()
    conn.close()

# Función para eliminar una opción de materia
def delete_option(option_id):
    conn = sqlite3.connect("school_schedule.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM options WHERE id = ?", (option_id,))
    conn.commit()
    conn.close()

# Función para actualizar la preferencia de una opción
def update_preference(option_id, new_preference):
    conn = sqlite3.connect("school_schedule.db")
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE options
    SET preference = ?
    WHERE id = ?
    ''', (new_preference, option_id))
    conn.commit()
    conn.close()

# Función para obtener todos los horarios generados
def get_all_schedules():
    conn = sqlite3.connect("school_schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schedules")
    schedules = cursor.fetchall()
    conn.close()
    return schedules