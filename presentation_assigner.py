
# coding=utf-8
"""
Ugly script to distribute presentations
"""

import glob
import csv
import random

preference = {}

counterOk = 0
counterFail = 0
errorFiles = []

for filename in glob.glob("pref_pres/*"):

    with open(filename) as file:
        try:
            content = file.read().strip()
            aux = content.split("-")

            if len(aux) == 2:
                session = int(aux[1])
            else:
                lastChar = aux[0][-1]
                session = int(lastChar)
                if session == 0:
                    raise Exception()

            if session >= 1 and session <= 9:
                preference[filename] = session
                counterOk += 1
            else:
                raise Exception()

        except:
            print("Error en archivo: " + filename)
            counterFail += 1
            errorFiles += [filename]

print()
print("Archivos procesados correctamente:", counterOk)
print("Archivos que no pudieron ser procesados:", counterFail)
print()
print("Archivos con errores:")
for filename in errorFiles:
    print(filename)
print()

sessionCandidates = {}

for student, session in preference.items():
    if session in sessionCandidates:
        sessionCandidates[session] += [student]
    else:
        sessionCandidates[session] = [student]


sessions = []
sessions += ["Sesión 0 es inválida"]
sessions += ["Sesión 1: 2019.04.09 - Tarea 1"]
sessions += ["Sesión 2: 2019.05.07 - Tarea 2"]
sessions += ["Sesión 3: 2019.06.11 - Tarea 3"]
sessions += ["Sesión 4: 2019.06.18 - Tareas 1, 2 o 3"]
sessions += ["Sesión 5: 2019.06.20 - Tareas 1, 2 o 3"]
sessions += ["Sesión 6: 2019.06.21 - Tareas 1, 2 o 3"]
sessions += ["Sesión 7: 2019.06.25 - Tarea 4"]
sessions += ["Sesión 8: 2019.06.27 - Tarea 4"]
sessions += ["Sesión 9: 2019.06.28 - Tarea 4"]


for session, students in sessionCandidates.items():
    print(sessions[session], ": ", len(students), "estudiantes")

    for student in students:
        print(student)
    print()

noPreference = []
with open('nomina.csv', encoding="utf8") as f:
    reader = csv.reader(f, dialect='excel')
    i = 0
    for row in reader:
        if i > 0:
            name = row[0]
            filename = name\
                .replace(" ", "_")\
                .replace(",", "_")\
                .replace("á","a")\
                .replace("é","e")\
                .replace("í","i")\
                .replace("ó","o")\
                .replace("ú","u")\
                .replace("Á","A")\
                .replace("É","E")\
                .replace("Í","I")\
                .replace("Ó","O")\
                .replace("Ú","U")

            pref = None
            for studentPreference in preference.keys():
                if filename in studentPreference:
                    pref = preference[studentPreference]
                    break

            #print(filename, "==>", pref)

            if pref == None:
                noPreference += [filename]
        i += 1


print("Estudiantes sin preferencia:", len(noPreference))
for student in noPreference:
    print(student)
print()

# Asignación final!

PRESENTATIONS_PER_SESSION = 10
NUMBER_OF_SESSIONS = 9

quota = {}
sessionStudents = {}
nonAssignedStudents = []

print("Revisando sobre cupos...")
for session, students in sessionCandidates.items():

    if (len(students) <= PRESENTATIONS_PER_SESSION):
        quota[session] = len(students) - PRESENTATIONS_PER_SESSION
        sessionStudents[session] = students

    else:
        print("Sesión", session, "con sobre cupo")
        quota[session] = 0
        random.shuffle(students)
        sessionStudents[session] = students[0:10]
        nonAssignedStudents += students[10:-1]

nonAssignedStudents += noPreference

print()
print("Asignando sesiones...")

random.shuffle(nonAssignedStudents)

for sessionId in range(1,10):
    while len(sessionStudents[sessionId]) < PRESENTATIONS_PER_SESSION and len(nonAssignedStudents) > 0:
        student = nonAssignedStudents.pop()
        print("Asignando sesión", sessionId, "a estudiante", student)
        sessionStudents[sessionId] += [student]

if len(nonAssignedStudents) != 0:
    print("Error: No se le ha asignado una sesión a los siguientes alumnos:")
    for student in nonAssignedStudents:
        print(student)
    raise Exception()

print()
print("=== Asignación Final ===")
print()
for session, students in sessionStudents.items():
    print(sessions[session], ": ", len(students), "estudiantes")

    for student in students:
        print(student)
    print()


if len(nonAssignedStudents) != 0:
    print("Error: No se le ha asignado una sesión a los siguientes alumnos:")
    for student in nonAssignedStudents:
        print(student)
    raise Exception()

