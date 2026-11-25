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
    
        # in case the try except decide to raise error for idk what reason (due to my shitty code)
        #amount_to_give = int(input("How much do you want to give ? "))
        #if self.balance - amount_to_give >= 0:
        #    print("YOU SPENT ", amount_to_give)
        #    self.balance -=amount_to_give


#lets keep a and b cuz idk what to plug in rn
#TODO: when building the TUI, lets remove the a and b and put the values in the interface and not from the backend code here 
trans = Transaction(a,b)


class Budget(Transaction):
    def __init__(self, balance, amount_to_give) -> None:
        super().__init__(balance, amount_to_give)
    def record_transaction(self, balance):
        with open("../big_data.txt", "a", encoding="UTF-8") as file:
            # UHHH let me see if the ../ works in python 
            #TODO: run the operation 
            return 
    def read_the_budget(self):
        with open("../big_data.txt", "r", encoding="UTF-8") as fiel: #very creative I know 
            content = fiel.read()
        print(content)


