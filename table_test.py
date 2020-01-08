from table import Table
import random
import os
import myparser
from compilator import compilate


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

#def comp(arg1, arg2):
#    return bool(random.randint(0, 1))

#students.join(professions, comp)
#print(students)

prog = myparser.parse(
         '''
    SELECT DISTINCT to_Int(str(dfd + 2) * ('aaa' || qwe * 3))  , str(2) || (4 *2)
    FROM professions JOIN students s ON (str(1 + '22') >= col1) LEFT JOIN students ON (1=1 OR w <> 45) AND r + 3 > r FULL JOIN students ON 1=1
    WHERE (q = b OR asd > nj) 
        AND q > e  
        AND (www = t OR fgk >= ANY ( SELECT * FROM students WHERE NOT EXISTS(SELECT tratr FROM sas;) ; ) )
    ;
        ''')

print(*prog.tree, sep=os.linesep)
print(compilate([students, professions], prog))
