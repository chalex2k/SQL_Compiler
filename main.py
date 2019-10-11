import os
import myparser


def main():
    prog = myparser.parse(
        '''
        SELECT DISTINCT *
               FROM students, lecturers;
        ''')
    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()