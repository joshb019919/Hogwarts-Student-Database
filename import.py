"""Import data from characters.csv into a relational database.
Much of my understanding comes from: https://www.sqlitetutorial.net/"""

import sqlite3
import csv
from sys import argv
from sys import exit


def main() -> None:
    """Open csv file and database, populate db tables with students' names."""

    # If command line was inputted correctly.
    if comm_args() == 0:
        characters = argv[1]

        # If CSV file exists, do magic, else print as much.
        try:
            db = sqlite3.connect("students.db")
            read_students(characters, db)
            db.commit()
            db.close()
        except FileNotFoundError:
            print("CSV file not found")
            exit(2)

    # If command line was NOT imputted corectly.
    elif comm_args() == 1:
        print("Usage: python import.py filename.csv")
        exit(1)

    return


def comm_args() -> int:
    """Make sure of 2 command line args."""

    if len(argv) != 2:
        return 1
    else:
        return 0


def read_students(characters: str, db: sqlite3.Connection) -> None:
    """Open csv file and read students into database."""

    with open(characters, newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            # Skip header row.
            if row[0] == "name":
                continue

            # Database fieldnames as abstractions for the query.
            name = row[0].split()
            first, last = name[0], name[-1]
            middle = name[1] if len(name) == 3 else None
            house, birth = row[1], row[-1]

            db.execute("""INSERT INTO
                                students
                                (first, middle, last, house, birth)
                            VALUES
                                (?, ?, ?, ?, ?)""",
                       (first, middle, last, house, birth))

    return


main()