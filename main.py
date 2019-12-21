import os
import myparser


def main():
    prog = myparser.parse(
         '''
SELECT  'dfv' || (dfdf || a), 2 - (4 -2)
 FROM students, lecturers JOIN univers ON 2 + cale + 2 <> forl || 'ekbwf'
 WHERE (q = b OR asd > nj) AND q > e ;

        ''')
    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()
