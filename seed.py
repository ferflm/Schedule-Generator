import sqlite3

def seed_data():
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()

    # Insertar materias
    subjects = [
        "Bases de Datos 2",
        "Programación Móvil",
        "Redes de Computadoras 2",
        "Habilidades Directivas"
    ]
    for subject in subjects:
        cursor.execute("INSERT INTO subjects (name) VALUES (?)", (subject,))

    # Insertar opciones de materias
    options = [
        (1, "Juarez Robles Elizabeth", "2859", "Lunes y Miércoles", "17:00 - 19:00", 5),
        (1, "Mendoza Gonzalez Omar", "2860", "Martes y Jueves", "13:00 - 15:00", 3),
        (1, "Canto Gallo Rafael", "2861", "Lunes, Miércoles y Viernes", "19:00 - 20:20", 4),
        (2, "Campos Bravo Jorge Ivan", "2857", "Martes y Jueves", "17:00 - 19:00", 5),
        (2, "Camacho Alvarez Juan Carlos", "2858", "Lunes, Miércoles y Viernes", "14:30 - 16:00", 4),
        (3, "Torres Rodriguez Gerardo", "2857", "Martes y Jueves", "19:00 - 21:00", 4),
        (4, "Velasco Agustin Aaron", "2857", "Lunes y Miércoles", "13:00 - 15:00", 5),
    ]

    for option in options:
        cursor.execute('''
        INSERT INTO options (subject_id, professor_name, "group", days, time, preference)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', option)

    conn.commit()
    conn.close()
    print("Datos de prueba insertados correctamente.")

if __name__ == "__main__":
    seed_data()