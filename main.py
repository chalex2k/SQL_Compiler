import os
import myparser


def main():
    prog = myparser.parse(
         '''
SELECT DISTINCT name
            FROM students 
            WHERE name = surname OR
             name > surname AND student_id <> mark_id AND rating >= min_r;

        ''')
    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()
