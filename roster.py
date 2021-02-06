"""Query and display the Hogwarts students by requested house.

Must run import.py first to create sqlite database from characters.csv."""

import sqlite3
from sys import argv
from sys import exit


def main() -> None:
    """Check proper commands, open db, and display students."""

    # If 2, invalid house name.  If 1, invalid args.  Else, go.
    if comm_line() == 2:
        print("Invalid house")
        exit(2)
    elif comm_line() == 1:
        print("Usage: python roster.py house")
        exit(1)
    else:
        house = argv[1].lower()
        db = sqlite3.connect("students.db")
        students = query(db)

        for student in students:
            # If student is in requested house, display.
            if name(student, house):
                print(name(student, house))

        db.close()
    return


def comm_line() -> int:
    """Make sure command line args are up and up."""

    houses = ["gryffindor", "ravenclaw", "hufflepuff", "slytherin"]

    if len(argv) != 2:
        return 1
    elif argv[1].lower() not in houses:
        return 2
    else:
        return 0


def name(student: str, house: str) -> str:
    """Select how to display which student."""

    # Abstractions.
    first, middle, last = student[0], student[1], student[2]
    birth = student[3]
    test_case = student[4].lower()
    output = (f"{first} {middle} {last}, born {birth}"
              if type(middle) == str
              else f"{first} {last}, born {birth}")

    return output if test_case == house else None


def query(db: sqlite3.Connection) -> sqlite3.Cursor:
    """Query Hogwarts students, order by last, first."""

    students = db.execute("""
        SELECT
            first,
            CASE middle WHEN 'None' THEN '' ELSE middle END,
            last,
            birth,
            house
        FROM
            students
        ORDER BY
            last,
            first""")

    return students


main()