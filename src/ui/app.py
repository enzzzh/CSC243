#Framework: textual (https://github.com/Textualize/textual) thank you 
#Run with: python app.py  (after installing textual)

import sys
import os

# make src/ importable so we can use the data intermediary
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Horizontal, Vertical, ScrollableContainer

from data_api import snapshot

def _col(row, index, default=""):
    return row[index] if index < len(row) else default


# These hold the latest snapshot; sync_state() refills them on every tick.
RAW_TRANSACTIONS = []
CATEGORIES = {}
TOP_CATEGORY = ("None", 0.0)
TOTAL_SPENT_TODAY = 0.0
CONSUMER_SCALE = 0.0
REFRESH_SECONDS = 1


def sync_state():
    global RAW_TRANSACTIONS, CATEGORIES, TOP_CATEGORY, TOTAL_SPENT_TODAY, CONSUMER_SCALE
    data = snapshot()
    RAW_TRANSACTIONS = data["rows"]
    CATEGORIES = data["categories"]
    TOP_CATEGORY = data["top"]
    TOTAL_SPENT_TODAY = data["total"]
    CONSUMER_SCALE = data["scale"]


class CategoryGraph(Static): #shiny components for non technical monkeys
    def compose(self) -> ComposeResult:
        yield Label("Spending by category", id="graph-title")

    def show(self) -> None:
        max_amount = max(CATEGORIES.values()) if CATEGORIES else 1
        lines = []
        for name, amount in CATEGORIES.items():
            bar_len = int((amount / max_amount) * 30) if max_amount else 0
            bar = "#" * bar_len
            lines.append(f"{name:12} |{bar} {amount:,.2f}")
        self.update("\n".join(lines))


class TopCategory(Static): #look out 
    def show(self) -> None:
        name, amount = TOP_CATEGORY
        self.update(f"Top category: {name}  ({amount:,.2f})")


class DailyTotal(Static):
    def show(self) -> None:
        self.update(f"Total spent today: {TOTAL_SPENT_TODAY:,.2f}")


class ConsumerScale(Static):
    def show(self) -> None:
        pos = int(CONSUMER_SCALE * 40)
        scale = "-" * pos + "o" + "-" * (40 - pos)
        self.update(
            f"Cheapskate  [{scale}]  Degenerate consumer\n"
            f"Value: {CONSUMER_SCALE:.2f}"
        )


class TransactionFeed(Static): #raw csv data piped straight from the "API" 
    def show(self) -> None:
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

    def on_mount(self) -> None:
        self.sync_from_csv()
        self.set_interval(REFRESH_SECONDS, self.sync_from_csv)

    def sync_from_csv(self) -> None:
        sync_state()
        self.query_one(CategoryGraph).show()
        self.query_one(TopCategory).show()
        self.query_one(DailyTotal).show()
        self.query_one(ConsumerScale).show()
        self.query_one(TransactionFeed).show()


if __name__ == "__main__":
    app = SpendingApp()
    app.run()
