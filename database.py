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
def getAllSubjects():
    try:
        conn = sqlite3.connect("schedule.db")
        cursor = conn.cursor()

        # Obtener todas las materias junto con sus opciones de horarios
        cursor.execute("""
        SELECT s.id, s.name, o.id, o.professor_name, o.group_name, o.days, o.time, o.preference
        FROM subjects s
        LEFT JOIN options o ON s.id = o.subject_id
        """)

        subjects = cursor.fetchall()
        conn.close()

        # Organizar los resultados en una estructura más fácil de manejar
        subjects_dict = {}

        for subject_id, subject_name, option_id, professor_name, group_name, days, time, preference in subjects:
            # Si la materia no existe en el diccionario, la agregamos
            if subject_id not in subjects_dict:
                subjects_dict[subject_id] = {
                    'name': subject_name,
                    'options': []
                }

            # Agregar la opción de horario a la materia correspondiente
            subjects_dict[subject_id]['options'].append({
                'id': option_id,
                'professor': professor_name,
                'group': group_name,
                'days': days.split(', '),  # Convertir los días en lista separando por coma
                'time': time,
                'preference': preference
            })

        # Devolver las materias con sus opciones en formato de lista
        return list(subjects_dict.values())
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return []

# Función para obtener todas las opciones de una materia específica
def getOptionsBySubject(subject_id):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM options WHERE subject_id = ?", (subject_id,))
    options = cursor.fetchall()
    conn.close()
    return options

# Función para agregar una nueva materia
def addSubject(name):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subjects (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

# Función para agregar una nueva opción de materia
def addOption(subject_id, professor_name, group, days, time, preference):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO options (subject_id, professor_name, "group", days, time, preference)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (subject_id, professor_name, group, days, time, preference))
    conn.commit()
    conn.close()

# Función para eliminar una opción de materia
def deleteOption(option_id):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM options WHERE id = ?", (option_id,))
    conn.commit()
    conn.close()

# Función para actualizar la preferencia de una opción
def updatePreference(option_id, new_preference):
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE options
    SET preference = ?
    WHERE id = ?
    ''', (new_preference, option_id))
    conn.commit()
    conn.close()

# Función para obtener todos los horarios generados
def getAllSchedules():
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schedules")
    schedules = cursor.fetchall()
    conn.close()
    return schedules
