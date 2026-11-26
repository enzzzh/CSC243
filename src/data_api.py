import csv
import os

DEFAULT_CSV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "big_data.csv")
)


def read_csv(path=DEFAULT_CSV_PATH): #comma seperated value, for the non technical monkeys reading this
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def load_transactions(path=DEFAULT_CSV_PATH): #actually return the data for the non empty rows seperated by comma
    rows = read_csv(path)
    return [row for row in rows if row and any(cell.strip() for cell in row)]
