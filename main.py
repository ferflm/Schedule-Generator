from database import getAllSubjects

def isValid(currSchedule, new_option):
    """
    Verifica si la opción de horario es válida en el horario actual.

    Args:
        currSchedule (list): Horario parcial con las opciones ya elegidas.
        new_option (dict): La nueva opción que queremos agregar.

    Returns:
        bool: True si es válida, False si se solapan.
    """
    for option in currSchedule:
        # Comprobar si los días de la nueva opción se solapan con las ya elegidas
        if any(day in option['days'] for day in new_option['days']):
            # Verificar si las horas se solapan (esto es solo un ejemplo, ajusta según el formato)
            if isTimeConflict(option['time'], new_option['time']):
                return False
    return True

def isTimeConflict(time1, time2):
    """
    Verifica si dos horarios se solapan.

    Args:
        time1 (str): El primer horario en formato "HH:MM - HH:MM".
        time2 (str): El segundo horario en formato "HH:MM - HH:MM".

    Returns:
        bool: True si se solapan, False si no.
    """
    # Este es un ejemplo básico. Necesitarás un manejo más preciso de los tiempos.
    start1, end1 = time1.split(' - ')
    start2, end2 = time2.split(' - ')
    
    # Convertir a formato de 24 horas para comparación (si es necesario)
    start1 = int(start1.replace(':', ''))
    end1 = int(end1.replace(':', ''))
    start2 = int(start2.replace(':', ''))
    end2 = int(end2.replace(':', ''))
    
    return not (end1 <= start2 or end2 <= start1)


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