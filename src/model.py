import csv
a = int(input())
b = int(input())
class Transaction:
    def __init__(self, balance, amount_to_give) -> None:
        self.balance = balance
        self.amount_to_give = amount_to_give

    def do_the_transaction(self) -> bool :
        try:
            amount = float(input())
        except ValueError:
            print("enter a normal number idiot")
            return False

        match (amount <= 0, amount > self.balance):
            case (True, True):
                print("Too poor for this ")
                return False
            case (True, False):
                print("what is this, infinite money glitch ???")
                return False
            case (False, True):
                print("Too poor for this ")
            case (False, False):
                self.balance -= amount 
                print(f"You spent {self.amount_to_give}, you still haave {self.balance} left")
                return True
            case _:
                print("?")
                return False
       

       #THIS CODE AGE LIKE MILK
        #    |
        #    v

        # in case the try except decide to raise error for idk what reason (due to my shitty code)
        #amount_to_give = int(input("How much do you want to give ? "))
        #if self.balance - amount_to_give >= 0:
        #    print("YOU SPENT ", amount_to_give)
        #    self.balance -=amount_to_give


#lets keep a and b cuz idk what to plug in rn
#TODO: when building the TUI, lets remove the a and b and put the values in the interface and not from the backend code here

#TODO: Why not add categories for each and every thing we do ? and what if we record earnings also ? like a NORMAL MONEY TRACKING APP
trans = Transaction(a,b)


class Budget(Transaction):
    cats = {}
    roles = {}
    def __init__(self, balance, amount_to_give) -> None:
        super().__init__(balance, amount_to_give)
    def cat(self, name):
        if name not in self.cats:
            self.cats[name] = len(self.cats)
        return self.cats[name]
    def role(self, name):
        if name not in self.roles:
            self.roles[name] = len(self.roles)
        return self.roles[name]
    def record_transaction(self, amount_b4, amount_after, status, category, role_name):
        with open("../big_data.csv", "a", newline="", encoding="UTF-8") as file:
            writer = csv.writer(file)
            writer.writerow([amount_b4, amount_after, status, self.cat(category), self.role(role_name)])
            return 
    def read_the_budget(self):
        with open("../big_data.csv", "r", encoding="UTF-8") as fiel:
            content = fiel.read()
        print(content)


