from database import getAllSubjects
from datetime import datetime

def isValid(currSchedule, option):
    for scheduled_option in currSchedule:
        if isConflicting(scheduled_option, option):
            return False
    return True

def isConflicting(option1, option2):
     # Comparar los días
    common_days = set(option1['days']).intersection(option2['days'])
    if not common_days:
        return False
    
    # Convertir las horas a objetos datetime para compararlas
    time1_start = datetime.strptime(option1['time'].split(' - ')[0], "%H:%M")
    time1_end = datetime.strptime(option1['time'].split(' - ')[1], "%H:%M")
    time2_start = datetime.strptime(option2['time'].split(' - ')[0], "%H:%M")
    time2_end = datetime.strptime(option2['time'].split(' - ')[1], "%H:%M")
    
    # Verificar si hay solapamiento
    if time1_start < time2_end and time2_start < time1_end:
        return True  # Hay un solapamiento
    
    return False


def generateSchedules(subjects, currSchedule = [], allSchedules = []):
    """
    Genera todos los horarios posibles usando backtracking.

    Args:
        subjects (list): Lista de materias con sus opciones de horario.
        currSchedule (list): Horario parcial construido.
        allSchedules (list): Lista de horarios válidos generados.

    Returns:
        list: Lista de horarios válidos.
    """
    # Si el horario está completo (es decir, hemos asignado todas las materias)
    if len(currSchedule) == len(subjects):
        # Agregar el horario completo a la lista de soluciones
        allSchedules.append(currSchedule.copy())
        return
    
    # Obtener la materia actual
    current_subject = subjects[len(currSchedule)]
    
    # Iterar sobre las opciones de la materia actual
    for option in current_subject['options']:
        # Verificar si la opción es válida en el horario actual
        if isValid(currSchedule, option):
            # Agregar la opción al horario parcial
            currSchedule.append(option)
            # Continuar con la siguiente materia
            generateSchedules(subjects, currSchedule, allSchedules)
            # Retroceder para probar otras opciones
            currSchedule.pop()

subjects = getAllSubjects()
allSchedules = []
generateSchedules(subjects, [], allSchedules)

for idx, schedule in enumerate(allSchedules):
        print(f"\nHorario #{idx + 1}:")
        for option in schedule:
            # Imprimir los detalles de cada opción en el horario
            print(f"  Materia: {option['id']}")
            print(f"    Profesor: {option['professor']}")
            print(f"    Grupo: {option['group']}")
            print(f"    Días: {', '.join(option['days'])}")
            print(f"    Horario: {option['time']}")
            print(f"    Preferencia: {option['preference']}")
        print("-" * 40)  # Separador entre horarios