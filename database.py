import sqlite3

conn = sqlite3.connect("schedule.db")

cursor = conn.cursor()

# Crear tabla de materias con session_id
cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        session_id TEXT NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions (id)
    );
''')

# Crear tabla de opciones con session_id
cursor.execute('''
    CREATE TABLE IF NOT EXISTS options (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        professor_name TEXT NOT NULL,
        group_name TEXT NOT NULL,
        days TEXT NOT NULL,
        time TEXT NOT NULL,
        preference INTEGER DEFAULT 0,
        session_id TEXT NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES subjects (id),
        FOREIGN KEY (session_id) REFERENCES sessions (id)
    );
''')

# Crear tabla de sesiones
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
''')

# Crear tabla de horarios generados
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

# Función para obtener todas las materias por session_id
def getAllSubjects(session_id):
    try:
        conn = sqlite3.connect("schedule.db")
        cursor = conn.cursor()

        # Obtener todas las materias junto con sus opciones de horarios por sesión
        cursor.execute("""
        SELECT s.id, s.name, o.id, o.professor_name, o.group_name, o.days, o.time, o.preference
        FROM subjects s
        LEFT JOIN options o ON s.id = o.subject_id
        WHERE s.session_id = ?
        """, (session_id,))

        subjects = cursor.fetchall()
        print(f"Resultados de la consulta: {subjects}")
        conn.close()

        # Organizar los resultados en una estructura más fácil de manejar
        subjects_dict = {}

        for subject_id, subject_name, option_id, professor_name, group_name, days, time, preference in subjects:
            if subject_id not in subjects_dict:
                subjects_dict[subject_id] = {
                    'name': subject_name,
                    'options': []
                }

            if option_id is not None:
                subjects_dict[subject_id]['options'].append({
                    'id': option_id,
                    'professor': professor_name,
                    'group': group_name,
                    'days': days.split(' '),
                    'time': time,
                    'preference': preference
                })

        return list(subjects_dict.values())
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return []

# Función para agregar una nueva materia
def addSubject(name, session_id):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subjects (name, session_id) VALUES (?, ?)", (name, session_id))
    conn.commit()
    conn.close()

# Función para agregar una nueva opción de materia
def addOption(subject_id, professor_name, group, days, time, preference, session_id):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO options (subject_id, professor_name, group_name, days, time, preference, session_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (subject_id, professor_name, group, days, time, preference, session_id))
    conn.commit()
    conn.close()

# Función para eliminar una opción de materia
def deleteOption(option_id, session_id):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM options WHERE id = ? AND session_id = ?", (option_id, session_id))
    conn.commit()
    conn.close()

# Función para actualizar la preferencia de una opción
def updatePreference(option_id, new_preference, session_id):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE options
    SET preference = ?
    WHERE id = ? AND session_id = ?
    ''', (new_preference, option_id, session_id))
    conn.commit()
    conn.close()

# Función para agregar una nueva sesión
def addSession(session_id):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (id) VALUES (?)", (session_id,))
    conn.commit()
    conn.close()

# Función para obtener todas las sesiones
def getAllSessions():
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions")
    sessions = cursor.fetchall()
    conn.close()
    return sessions

# Función para obtener todos los horarios generados por session_id
def getAllSchedules(session_id):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schedules WHERE session_id = ?", (session_id,))
    schedules = cursor.fetchall()
    conn.close()
    return schedules
