import os
import myparser


def main():
    prog = myparser.parse(
         '''
         SELECT DISTINCT name, surname, mark
            FROM students FULL OUTER JOIN marks ON stud_id = mark_id, lecturers
            WHERE name = surname OR name = surname AND student_id <> mark_id AND ratind >= min_r
        ;
        ''')
    print(*prog.tree, sep=os.linesep)


if __name__ == "__main__":
    main()