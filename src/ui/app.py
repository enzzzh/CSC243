#Framework: textual (https://github.com/Textualize/textual) thank you 
#Run with: python app.py  (after installing textual)

import sys
import os

# make src/ importable so we can use the data intermediary
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Horizontal, Vertical, ScrollableContainer

from data_api import load_transactions


# ---------------------------------------------------------------------------
# Data intermediary: barebone CSV -> UI. No hard cases, just raw rows.
# Columns (by position): amount_b4 | amount_after | status | category | role
# ---------------------------------------------------------------------------
RAW_TRANSACTIONS = load_transactions()


def _num(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def _col(row, index, default=""):
    return row[index] if index < len(row) else default


# Simple aggregates computed straight from the CSV. Falls back to the old
CATEGORIES = {}
for row in RAW_TRANSACTIONS:
    name = _col(row, 3) or "uncategorized"
    spent = _num(_col(row, 0, 0)) - _num(_col(row, 1, 0))
    CATEGORIES[name] = CATEGORIES.get(name, 0.0) + spent

if not CATEGORIES:
    CATEGORIES = {
        "Food": 120.50,
        "Transport": 45.00,
        "Entertainment": 80.00,
        "Rent": 900.00,
        "Utilities": 120.00,
    }

TOP_CATEGORY = max(CATEGORIES.items(), key=lambda kv: kv[1]) if CATEGORIES else ("None", 0.0)
TOTAL_SPENT_TODAY = (
    sum(_num(_col(r, 0, 0)) - _num(_col(r, 1, 0)) for r in RAW_TRANSACTIONS)
    or 245.75
)

# Cheapskate (0.0) <----------------------> Degenerate consumer (1.0)
CONSUMER_SCALE = 0.45


class CategoryGraph(Static): #shiny components for non technical monkeys
    def compose(self) -> ComposeResult:
        yield Label("Spending by category", id="graph-title")

    def on_mount(self) -> None:
        max_amount = max(CATEGORIES.values()) if CATEGORIES else 1
        lines = []
        for name, amount in CATEGORIES.items():
            bar_len = int((amount / max_amount) * 30) if max_amount else 0
            bar = "#" * bar_len
            lines.append(f"{name:12} |{bar} {amount:,.2f}")
        self.update("\n".join(lines))


class TopCategory(Static): #look out 
    def on_mount(self) -> None:
        name, amount = TOP_CATEGORY
        self.update(f"Top category: {name}  ({amount:,.2f})")


class DailyTotal(Static):
    def on_mount(self) -> None:
        self.update(f"Total spent today: {TOTAL_SPENT_TODAY:,.2f}")


class ConsumerScale(Static):
    def on_mount(self) -> None:
        pos = int(CONSUMER_SCALE * 40)
        scale = "-" * pos + "o" + "-" * (40 - pos)
        self.update(
            f"Cheapskate  [{scale}]  Degenerate consumer\n"
            f"Value: {CONSUMER_SCALE:.2f}"
        )


class TransactionFeed(Static): #raw csv data piped straight from the "API" 
    def on_mount(self) -> None:
        lines = [
            "(amount_b4 | amount_after | status | category | role)",
            "-" * 55,
        ]
        for row in RAW_TRANSACTIONS:
            lines.append(
                f"{_col(row, 0):>9} | "
                f"{_col(row, 1):>11} | "
                f"{_col(row, 2):<7} | "
                f"cat={_col(row, 3):<4} | "
                f"role={_col(row, 4)}"
            )
        self.update("\n".join(lines))


class SpendingApp(App):
    TITLE = "Spending Tracker"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with Horizontal():
            with Vertical():
                yield CategoryGraph()
                yield TopCategory()
            with Vertical():
                yield DailyTotal()
                yield ConsumerScale()

        yield ScrollableContainer(TransactionFeed(), id="feed")


if __name__ == "__main__":
    app = SpendingApp()
    app.run()
