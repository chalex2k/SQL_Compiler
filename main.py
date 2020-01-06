import os
import myparser


def main():
    prog = myparser.parse(
         '''
SELECT DISTINCT to_int((dfd + 2) * ('aaa' || qwe * 3))  , str(2) || (4 *2)
 FROM students, lecturers JOIN univers ON NOT 2 + (cale + 2) = (forl || 'ekbwf') OR NOT 1=1 OR 1=1
 WHERE (q = b OR asd > nj) AND q > e AND (www = t OR wer > 3 OR fgk < 2);

        ''')
    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()
