from flask import Blueprint, jsonify, request, send_from_directory
from scheduleLogic import generateSchedules, getBestSchedules, filterValidSchedules
from database import getAllSubjects, addSession
from datetime import datetime
import sqlite3
import uuid

apiBlueprint = Blueprint('api', __name__)
db = "schedule.db"

@apiBlueprint.route('/api/options/<int:option_id>', methods=['DELETE'])
def deleteOption(option_id):
    try:
        # Obtener el session_id desde el encabezado
        session_id = request.headers.get('Session-Id')
        if not session_id:
            return jsonify({"error": "Session-Id es obligatorio"}), 400

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Validar que la opción pertenece a la sesión actual
        cursor.execute("""
            SELECT id FROM options WHERE id = ? AND session_id = ?
        """, (option_id, session_id))
        option = cursor.fetchone()

        if not option:
            conn.close()
            return jsonify({"error": "Opción no encontrada o no pertenece a la sesión actual"}), 404

        # Eliminar la opción
        cursor.execute("DELETE FROM options WHERE id = ?", (option_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Opción eliminada correctamente"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# Ruta para servir index.html
@apiBlueprint.route("/")
def serveIndex():
    return send_from_directory("../app/static", "index.html")

# Endpoint para crear una sesión
@apiBlueprint.route("/api/session", methods=["POST"])
def createSession():
    try:
        session_id = str(uuid.uuid4())
        addSession(session_id)
        return jsonify({"session_id": session_id}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    
# Endpoint para generar horarios
@apiBlueprint.route('/api/schedules', methods=['GET'])
def generateSchedulesEndpoint():
    try:
        session_id = request.headers.get('Session-Id')
        if not session_id:
            return jsonify({"error": "Session-Id es obligatorio"}), 400

        # Obtener materias y opciones relacionadas con la sesión
        subjects_list = getAllSubjects(session_id)
        print(subjects_list)
        if not subjects_list:
            return jsonify({"error": "No se encontraron materias para esta sesión"}), 404

        allSchedules = []
        generateSchedules(subjects_list, [], allSchedules)
        print(allSchedules)

        validSchedules = filterValidSchedules(allSchedules)
        if not validSchedules:
            return jsonify({"error": "No se encontraron horarios válidos"}), 400

        schedules = getBestSchedules(validSchedules)
        print(schedules)
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
@apiBlueprint.route('/api/subjects', methods=['POST'])
def addSubject():
    try:
        session_id = request.headers.get('Session-Id')
        if not session_id:
            return jsonify({"error": "Session-Id es obligatorio"}), 400

        data = request.json
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
@apiBlueprint.route('/api/subjects/<int:subject_id>/options', methods=['POST'])
def addOption(subject_id):
    try:
        session_id = request.headers.get('Session-Id')
        if not session_id:
            return jsonify({"error": "Session-Id es obligatorio"}), 400

        data = request.json
        professor = data.get('professor')
        group_name = data.get('group_name')
        days = data.get('days')
        time = data.get('time')
        preference = data.get('preference', 0)

        if not all([professor, group_name, days, time]):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO options (subject_id, professor_name, group_name, days, time, preference, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (subject_id, professor, group_name, days, time, preference, session_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Opción agregada correctamente"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    
@apiBlueprint.route('/api/subjects', methods=['GET'])
def getSubjects():
    try:
        session_id = request.headers.get('Session-Id')
        if not session_id:
            return jsonify({"error": "Session-Id es obligatorio"}), 400

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Obtener materias
        cursor.execute("""
            SELECT id, name FROM subjects WHERE session_id = ?
        """, (session_id,))
        subjects = cursor.fetchall()

        # Formatear las materias
        subjects_response = []
        for subject in subjects:
            subject_id, subject_name = subject

            # Obtener opciones de la materia
            cursor.execute("""
                SELECT id, professor_name, group_name, days, time, preference
                FROM options WHERE subject_id = ?
            """, (subject_id,))
            options = cursor.fetchall()

            # Formatear opciones
            options_response = [
                {
                    "id": option[0],
                    "professor": option[1],
                    "group": option[2],
                    "days": option[3],
                    "time": option[4],
                    "preference": option[5],
                }
                for option in options
            ]

            # Agregar materia con opciones
            subjects_response.append({
                "id": subject_id,
                "name": subject_name,
                "options": options_response,
            })

        conn.close()
        return jsonify(subjects_response), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

@apiBlueprint.route('/api/subjects/<int:subject_id>', methods=['DELETE'])
def deleteSubject(subject_id):
    try:
        # Obtener el session_id desde el encabezado
        session_id = request.headers.get('Session-Id')
        if not session_id:
            return jsonify({"error": "Session-Id es obligatorio"}), 400

        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Validar que la materia pertenece a la sesión actual
        cursor.execute("""
            SELECT id FROM subjects WHERE id = ? AND session_id = ?
        """, (subject_id, session_id))
        subject = cursor.fetchone()

        if not subject:
            conn.close()
            return jsonify({"error": "Materia no encontrada o no pertenece a la sesión actual"}), 404

        # Eliminar las opciones de la materia
        cursor.execute("DELETE FROM options WHERE subject_id = ?", (subject_id,))

        # Eliminar la materia
        cursor.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Materia y sus opciones eliminadas correctamente"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
