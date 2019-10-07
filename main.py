import os
import myparser


def main():
    prog = myparser.parse ('''
        SELECT name 
        FROM students lecturer  managers
        ''')
    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()