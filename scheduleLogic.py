from datetime import datetime

def isConflicting(option1, option2):
    common_days = set(option1['days']).intersection(set(option2['days']))
    if not common_days:
        return False

    time1_start = datetime.strptime(option1['time'].split(' - ')[0], "%H:%M")
    time1_end = datetime.strptime(option1['time'].split(' - ')[1], "%H:%M")
    time2_start = datetime.strptime(option2['time'].split(' - ')[0], "%H:%M")
    time2_end = datetime.strptime(option2['time'].split(' - ')[1], "%H:%M")

    for day in common_days:
        if time1_start < time2_end and time2_start < time1_end:
            return True
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

def getBestSchedules(validSchedules, max_results=3):
    if not validSchedules:
        return []

    schedules_with_preference = []
    for schedule in validSchedules:
        if len(schedule) > 0:  # Verifica si el horario no está vacío
            avg_preference = sum(option['preference'] for option in schedule) / len(schedule)
            schedules_with_preference.append((schedule, avg_preference))
        else:
            schedules_with_preference.append((schedule, 0))  # O maneja el caso de otra manera

    schedules_with_preference.sort(key=lambda x: x[1], reverse=True)
    best_schedules = [schedule for schedule, _ in schedules_with_preference[:max_results]]
    return best_schedules

