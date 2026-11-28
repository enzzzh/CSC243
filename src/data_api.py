import csv
import os

DEFAULT_CSV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "big_data.csv")
)


def read_csv(path=DEFAULT_CSV_PATH): #comma seperated value, for the non technical monkeys reading this
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def load_transactions(path=DEFAULT_CSV_PATH): #actually return the data for the non empty rows seperated by comma
    if not os.path.exists(path): #a refresh must not kill the UI if the big data disappeard 
        return []
    rows = read_csv(path)
    return [row for row in rows if row and any(cell.strip() for cell in row)]


def _num(value, default=0.0): #CSV cells are text, the UI wants numbers
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def _col(row, index, default=""):
    return row[index] if index < len(row) else default


def snapshot(path=DEFAULT_CSV_PATH): #one call = every value the UI displays, recomputed from the CSV
    rows = load_transactions(path)

    categories = {}
    for row in rows:
        name = _col(row, 3) or "uncategorized"
        spent = _num(_col(row, 0, 0)) - _num(_col(row, 1, 0))
        categories[name] = categories.get(name, 0.0) + spent

    if not categories: #keep the demo data for an empty csv, in case shit go south
        categories = {
            "Food": 120.50,
            "Transport": 45.00,
            "Entertainment": 80.00,
            "Rent": 900.00,
            "Utilities": 120.00,
        }

    total = sum(_num(_col(r, 0, 0)) - _num(_col(r, 1, 0)) for r in rows) or 245.75
    started_with = sum(_num(_col(r, 0, 0)) for r in rows)
    top_name = max(categories, key=categories.get) # could have been done with a lambda function but who am I to judge 

    return {
        "rows": rows,
        "categories": categories,
        "top": (top_name, categories[top_name]),
        "total": total,
        "scale": min(1.0, total / started_with) if started_with else 0.45,
    }
