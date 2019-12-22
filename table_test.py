from table import Table
import random

data = [
    ['Name', 'Surname', 'Age', 'Kurs'],
    ['Alex', 'Chirkin', 19, 3],
    ['Varya', 'Gospodarikova', 18, 3],
    ['Lesya', 'Lipatova', 18, 1],
    ['Lex', 'Kuduhov', 22, 5],
    ['Alexander', 'Kozhuhov', 20, 3],
    ['Nikolay', 'Paukov', 20, 3],
    ['Vadim', 'Smagin', 18, 2],
    ['Ivan', 'Zaborskih', 20, 2],
    ['Olesya', 'Tranina', 21, 4],
    ['Ruslan', 'Pogorelov', 20, 3]
]
students = Table('students', data)
print(students)

data2 = [
    ['Profession', 'Company'],
    ['student', 'university'],
    ['developer', 'it company']
]

professions = Table('professions', data2)
print(professions)

def comp(arg1, arg2):
    return bool(random.randint(0, 1))

students.join(professions, comp)
print(students)
