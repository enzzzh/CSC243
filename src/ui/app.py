#Framework: textual (https://github.com/Textualize/textual) thank you 
#Run with: python app.py  (after installing textual)

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label, ProgressBar
from textual.containers import Horizontal, Vertical

# dummy data cuz im lazy
CATEGORIES = {
    "Food": 120.50,
    "Transport": 45.00,
    "Entertainment": 80.00,
    "Rent": 900.00,
    "Utilities": 120.00,
}

TOP_CATEGORY = ("Rent", 900.00)
TOTAL_SPENT_TODAY = 245.75

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
        scale = "-" * pos + "●" + "-" * (40 - pos)
        self.update(
            f"Cheapskate  [{scale}]  Degenerate consumer\n"
            f"Value: {CONSUMER_SCALE:.2f}"
        )


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


if __name__ == "__main__":
    app = SpendingApp()
    app.run()
