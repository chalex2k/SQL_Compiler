import os
import myparser


def main():
    prog = myparser.parse(
        '''
        SELECT DISTINCT * |
               FROM students;
        ''')
    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()