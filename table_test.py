from table import Table
import random
import os
import myparser
from compilator import compilate


data = [
    ['Name', 'Surname', 'Age', 'Kurs'],
    ['Alexander', 'Alexandrov', 19, 3],
    ['Ivan', 'Ivanov', 18, 3],
    ['Petr', 'Petrov', 18, 1],
    ['Alexey', 'Alexeev', 22, 5],
    ['Sergey', 'Sergeev', 20, 3],
    ['Nikolay', 'Nikolaev', 20, 3],
    ['Vadim', 'Vadimov', 18, 2],
    ['Andrey', 'Andreev', 20, 2],
    ['Pavel', 'Pavlov', 21, 4],
    ['Ruslan', 'Ruslanov', 20, 3]
]
students = Table('students', data)
print(students)

data2 = [
    ['Profession', 'Company', 'Age'],
    ['student', 'university', 22],
    ['developer', 'it company', 20]
]

professions = Table('professions', data2)
print(professions)

data3 = [
    ['Fio', 'Kurs'],
    ['Ivan Sergeevich', 1],
    ['Evgeniy Ivanovich', 2]
]

lecturers = Table('lecturers', data3)
print(lecturers)


#def comp(arg1, arg2):
#    return bool(random.randint(0, 1))

#students.join(professions, comp)
#print(students)   students.Surname = 'Petrov' OR p.Age = 20

prog = myparser.parse(
         '''
    SELECT DISTINCT to_Int(str(dfd + 2) * ('aaa' || qwe * 3))  , str(2) || (4 *2)
    FROM students s, professions p
    WHERE s.Kurs = 3 OR Surname = 'Alexandrov'
    GROUP BY Kurs
    ;
        ''')
#FROM students s1 JOIN professions s2 ON s1.Age  = s2.Age JOIN lecturers l ON l.Kurs = 1 OR l.Kurs = 2 AND s1.Name = 'Ivan'
print(*prog.tree, sep=os.linesep)
print(compilate([students, professions, lecturers], prog))
