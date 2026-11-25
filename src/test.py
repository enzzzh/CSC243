#TOO LAZY TO CHECK EVERYTHING BY HAND
import csv
import os
import sys
import io

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import Budget

TEST_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "big_data.csv")) #turns out ../ works in python (ah no its os librarby)

print(f"Test file: {TEST_FILE}\n")

# Start clean
if os.path.exists(TEST_FILE):
    os.remove(TEST_FILE)
    print("Removed existing big_data.csv")

old_stdin = sys.stdin

def feed_input(text):
    sys.stdin = io.StringIO(text)

def restore_stdin():
    sys.stdin = old_stdin

print("TEST 1:  A normal human being using the app (amount_b4=100, amount_after=90 -> SAVED)")

trans1 = Budget(100, 25)
amount_b4_1 = trans1.balance
feed_input("10\n")
result1 = trans1.do_the_transaction()
restore_stdin()
print(f"do_the_transaction returned: {result1}")

if result1:
    trans1.record_transaction(amount_b4_1, trans1.balance, "success")
    print("record_transaction called -> wrote to CSV")
else:
    print("record_transaction NOT called -> nothing written")

print("TEST 2: Failed - broke monkey (balance=10, amount=15 -> NOT SAVED)")

trans2 = Budget(10, 25)
amount_b4_2 = trans2.balance
feed_input("15\n")
result2 = trans2.do_the_transaction()
restore_stdin()
print(f"do_the_transaction returned: {result2}")

if result2:
    trans2.record_transaction(amount_b4_2, trans2.balance, "success")
    print("record_transaction called -> wrote to CSV")
else:
    print("record_transaction NOT called -> nothing written")

print("TEST 3: Failed - negative amount (amount=-5 -> NOT SAVED)")

trans3 = Budget(100, 25)
amount_b4_3 = trans3.balance
feed_input("-5\n")
result3 = trans3.do_the_transaction()
restore_stdin()
print(f"do_the_transaction returned: {result3}")

if result3:
    trans3.record_transaction(amount_b4_3, trans3.balance, "success")
    print("record_transaction called -> wrote to CSV")
else:
    print("record_transaction NOT called -> nothing written")

if os.path.exists(TEST_FILE):
    with open(TEST_FILE, "r", newline="", encoding="UTF-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            print(f"Row {i}: {row}")
else:
    print("File does not exist, what have we been doing this whole time ??")

print("\n" + "=" * 50) # im having brain damage reviewing everything now. I dont feel good at all
print("EXPECTED: Only 1 data row (100, 90.0, success)")
print("FAILED transactions should NOT appear")
print("=" * 50)
