import os
import myparser


def main():
    prog = myparser.parse(
         '''
SELECT DISTINCT count(*) + 2
 FROM students
;
        ''')
    print(*prog.tree, sep=os.linesep)
if __name__ == "__main__":
    main()
"""
SELECT a

SELECT A_

SELECT _a

SELECT ___

SELECT 24D // FALL

SELECT 2_

SELECT 3

SELECT 2.9

SELECT 0.0001

SELECT 3,2

SELECT a.b

SELECT a. // FALL

SELECT .a // FALL

SELECT 'aaa'

SELECT ' ' // FALL

SELECT 'as aK 2 d2 _'

SELECT '' // FALL


SELECT 'q' + 2 - 2

SELECT 1+1+1+1+1

SELECT 0 + a + 's'

SELECT 4 / 4 || 'ds'

SELECT a + b - c

SELECT a || a + a * a - a / a

SELECT 1 + 2 / 3

SELECT 1 * 2  - 3

SELECT 1 * 3 / 2

SELECT (1 + 2) * 3

SELECT (1+2) / (a || 'v')

SELECT int(1)

SELECT int( 2 + 'fsdf' )

SELECT str( scsdc || ('sdc' * 0))

SELECT int(str(int('qqq')))

SELECT *

SELECT *, '4'   // FALL

SELECT count(*)

SELECT count(*) + 2, a

SELECT a,b,c,2,3,4,'d'














SELECT DISTINCT To_Int( str(dfdrRr.c + 2.5 + 11) * (' a_ R0a' || qwe * 3))  , str(2) || (4 *2)



    SELECT DISTINCT to_Int(str(dfd + 2) * ('aaa' || qwe * 3))  , str(2) || (4 *2)
 FROM students, lecturers JOIN univers ON NOT 1<>1
 WHERE (q = b OR asd > nj) AND q > e AND (www = t OR fgk IN ( SELECT * FROM students; ) ; )
"""