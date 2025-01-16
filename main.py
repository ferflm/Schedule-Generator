from database import getAllSubjects
from datetime import datetime

def isConflicting(option1, option2):
    # Verificar si hay días comunes entre las dos opciones
    common_days = set(option1['days']).intersection(set(option2['days']))
    
    # Si no hay días comunes, no hay conflicto
    if not common_days:
        return False

    # Obtener los horarios de ambas opciones
    time1_start = datetime.strptime(option1['time'].split(' - ')[0], "%H:%M")
    time1_end = datetime.strptime(option1['time'].split(' - ')[1], "%H:%M")
    time2_start = datetime.strptime(option2['time'].split(' - ')[0], "%H:%M")
    time2_end = datetime.strptime(option2['time'].split(' - ')[1], "%H:%M")

    # Comprobar si hay solapamiento de horarios en los días comunes
    for day in common_days:
        if time1_start < time2_end and time2_start < time1_end:
            return True  # Hay conflicto en el horario

    return False

def isValidSchedule(schedule):
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            if isConflicting(schedule[i], schedule[j]):
                return False
    return True

def filterValidSchedules(allSchedules):
    valid_schedules = [schedule for schedule in allSchedules if isValidSchedule(schedule)]
    return valid_schedules

def generateSchedules(subjects, currSchedule=[], allSchedules=[]):
    if len(currSchedule) == len(subjects):
        allSchedules.append(currSchedule.copy())
        return

    current_subject = subjects[len(currSchedule)]

    for option in current_subject['options']:
        currSchedule.append(option)
        generateSchedules(subjects, currSchedule, allSchedules)
        currSchedule.pop()

# Obtener las materias y generar todos los horarios
subjects = getAllSubjects()
allSchedules = []
generateSchedules(subjects, [], allSchedules)

print(f"Se generaron {len(allSchedules)} horarios totales.")

validSchedules = filterValidSchedules(allSchedules)


for idx, schedule in enumerate(validSchedules):
    print(f"\nHorario #{idx + 1}:")
    for option in schedule:
        print(f"  Materia: {option['id']}")
        print(f"    Profesor: {option['professor']}")
        print(f"    Grupo: {option['group']}")
        print(f"    Días: {', '.join(option['days'])}")
        print(f"    Horario: {option['time']}")
        print(f"    Preferencia: {option['preference']}")
    print("-" * 40)

