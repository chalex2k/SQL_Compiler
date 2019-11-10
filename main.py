import os
import myparser


def main():
    prog = myparser.parse(
         '''
SELECT  'dfv' || (dfdf || a), 2 - (4 -2) ;

        ''')
    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()
