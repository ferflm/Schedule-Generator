from flask import Blueprint, jsonify, request
from scheduleLogic import generateSchedules, getBestSchedules, filterValidSchedules
from database import getAllSubjects
import sqlite3
import uuid

apiBlueprint = Blueprint('api', __name__)
db = "schedule.db"

# Endpoint para generar horarios
@apiBlueprint.route('/schedules', methods=['GET'])
def generateSchedulesEndpoint():
    try:
        # Obtener el session_id desde el encabezado o parámetro de consulta
        session_id = request.headers.get('Session-Id')
        print(f"Session ID recibido: {session_id}")
        if not session_id:
            return jsonify({"error": "Session-Id es obligatorio"}), 400

        subjects_list = getAllSubjects(session_id)
        
        if not subjects_list:
            return jsonify({"error": "No se encontraron materias para esta sesión"}), 404

        # Generar horarios
        allSchedules = []
        generateSchedules(subjects_list, [], allSchedules)
        
        # Verifica los horarios generados antes de filtrarlos
        if not allSchedules:
            return jsonify({"error": "No se generaron horarios válidos"}), 400

        validSchedules = filterValidSchedules(allSchedules)
        
        # Verifica los horarios válidos antes de pasarlos a getBestSchedules
        if not validSchedules:
            return jsonify({"error": "No se encontraron horarios válidos"}), 400

        schedules = getBestSchedules(validSchedules)

        # Formatear respuesta
        response = [
            {
                "schedule": [
                    {
                        "subject": option['id'],
                        "professor": option['professor'],
                        "group": option['group'],
                        "days": option['days'],
                        "time": option['time'],
                        "preference": option['preference']
                    }
                    for option in schedule
                ]
            }
            for schedule in schedules
        ]
        return jsonify({"schedules": response}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500


# Endpoint para agregar una materia
@apiBlueprint.route('/subjects', methods=['POST'])
def addSubject():
    try:
        data = request.json
        session_id = request.headers.get('Session-Id')
        if not session_id:
            return jsonify({"error": "Session-Id es obligatorio"}), 400

        name = data.get('name')
        if not name:
            return jsonify({"error": "El nombre de la materia es obligatorio"}), 400

        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO subjects (name, session_id) VALUES (?, ?)", (name, session_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Materia agregada correctamente"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para agregar una opción de materia
@apiBlueprint.route('/subjects/<int:subject_id>/options', methods=['POST'])
def addOption(subject_id):
    try:
        data = request.json
        session_id = request.headers.get('Session-Id')
        if not session_id:
            return jsonify({"error": "Session-Id es obligatorio"}), 400

        professor = data.get('professor')
        group = data.get('group')
        days = data.get('days')
        time = data.get('time')
        preference = data.get('preference', 0)

        if not all([professor, group, days, time]):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO options (subject_id, professor_name, group_name, days, time, preference, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (subject_id, professor, group, days, time, preference, session_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Opción agregada correctamente"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para crear una nueva sesión
@apiBlueprint.route('/sessions', methods=['POST'])
def createSession():
    try:
        session_id = str(uuid.uuid4())
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sessions (id) VALUES (?)", (session_id,))
        conn.commit()
        conn.close()
        return jsonify({"session_id": session_id}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
