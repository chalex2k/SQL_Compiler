import os
import myparser


def main():
    prog = myparser.parse(
         '''
SELECT DISTINCT to_int((dfd + 2) * ('aaa' || qwe * 3))  , str(2) || (4 *2)
 FROM students, lecturers JOIN univers ON NOT 1<>1
 WHERE (q = b OR asd > nj) AND q > e AND (www = t OR fgk IN ( SELECT * FROM students; ) );
        ''')
    """
    SELECT DISTINCT to_int((dfd + 2) * ('aaa' || qwe * 3))  , str(2) || (4 *2)
 FROM students, lecturers JOIN univers ON NOT 1<>1
 WHERE (q = b OR asd > nj) AND q > e AND (www = t OR fgk IN ( SELECT * FROM students; ) ; )"""
    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()
