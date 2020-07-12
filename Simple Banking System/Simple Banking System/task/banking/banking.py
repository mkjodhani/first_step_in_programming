import random
import sqlite3

conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS "card" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"number"	TEXT NOT NULL,
	"pin"	TEXT NOT NULL,
	"balance"	INTEGER NOT NULL DEFAULT 0
);""")
conn.commit()


class Account(object):
    def __init__(self,new_account,card_number=None):
        if new_account:
            self.CARD_NUMBER = self.generate_account_number()
            self.PIN = int(str(random.randint(1000, 9999)).zfill(4))
            self.balance = 0
            cur.execute(f"INSERT  INTO card(number,pin,balance) VALUES({str(self.CARD_NUMBER)} ,{self.PIN},{self.balance})")
            conn.commit()
        else:
            cur.execute(f"""SELECT * from card where number = {card_number}""")
            data=cur.fetchone()
            self.CARD_NUMBER = str(data[1])
            self.PIN =int(data[2])
            self.balance = int(data[3])

    def check_luhn_algo(self,number):
        digits=list(int(char) for char in number)
        print(digits)
        for i in range(0,len(digits),2):
            digits[i]=digits[i]*2
        print(digits)
        for i in range(0,len(digits),2):
            if len(str(digits[i]))>1:
                digits[i]=sum(list(int(char) for char in str(digits[i])))
        print(digits)
        print(sum(digits))
        s=sum(digits)-digits[-1]
        CS="0" if (s)%10 ==0 else str(10-(s)%10)
        return CS == str(number[-1]):
    

    def add_income(self):
        print("Enter income:")
        income=int(input())
        cur.execute(f"""UPDATE card SET balance = balance + {income} WHERE number = "{str(self.CARD_NUMBER)}";""")
        conn.commit()
        print("Income was added")

    def do_transfer(self):
        print("Enter The Card Number:")
        transfer_number = input()
        cur.execute("""SELECT number from card""")
        all_number=list()
        for tuple in cur.fetchall():
            all_number.append(tuple[0])
        if not self.check_luhn_algo(transfer_number):
            print("“Probably you made mistake in the card number. Please try again!”")
        elif str(transfer_number) == self.CARD_NUMBER:
            print("You can't transfer money to the same account!")
        elif transfer_number in all_number:
            print("Enter how much money you want to transfer:")
            money=int(input())
            cur.execute(f"""SELECT balance From card Where number is {self.CARD_NUMBER}""")
            current_balance=cur.fetchone()[0]
            if current_balance>money:
                cur.execute(
                    f"""UPDATE card SET balance=balance + {money} WHERE number = {transfer_number};""")
                cur.execute(
                    f"""UPDATE card SET balance=balance - {money} WHERE number = {self.CARD_NUMBER};""")
                conn.commit()
                print("Success!")
            else:
                print("Not enough money!")
        else:
            print("Such a card does not exist.")

    def generate_account_number(self):
        MII_BIN = "400000"
        AI = str(random.randint(1, 999999999)).zfill(9)
        number = MII_BIN + AI
        digits = list(int(char) for char in number)
        for i in range(0, len(digits), 2):
            digits[i] = digits[i] * 2
        for i in range(0, len(digits), 2):
            if len(str(digits[i])) > 1:
                digits[i] = sum(list(int(char) for char in str(digits[i])))
        if sum(digits) % 10 == 0:
            CS = "0"
        else:
            CS = str(10 - sum(digits) % 10)
        number += CS
        return number

    def menu(self):
        print("""1. Balance
2.Add income
3.Do transfer
4.Close account
5. Log out
0. Exit""")

    def get_card_number(self):
        return self.CARD_NUMBER

    def get_pin_number(self):
        return self.PIN
    def get_balance(self):
        cur.execute(f"""SELECT balance from card where number = {self.CARD_NUMBER}""")
        self.balance=int(cur.fetchone()[0])
        return self.balance
    def print_message(self):
        print("Your card has been created")
        print("Your card number:")
        print(self.CARD_NUMBER)
        print("Your card PIN:")
        print(self.PIN)
    def close_account(self):
        cur.execute(f"""DELETE FROM card WHERE number = {self.CARD_NUMBER}""")
        conn.commit()
        print("The account has been closed!")
    def log_in(self):
        print("You have successfully logged in!")
        while True:
            self.menu()
            choice = int(input())
            if choice == 1:
                print("Balance: " + str(self.get_balance()))
            elif choice ==2:
                self.add_income()
            elif choice ==3:
                self.do_transfer()
            elif choice ==4:
                self.close_account()
            elif choice == 5:
                print("You have successfully logged out!")
                break
            elif choice == 0:
                print("Bye!")
                exit()


def account_avilable(card_number):
    cur.execute("""SELECT number FROM card""")
    accounts=cur.fetchall()
    for account in accounts:
        if account[0] == str(card_number):
            return True
    return False


def Menu():
    print("""1. Create an account
2. Log into account
0. Exit""")


while True:
    Menu()
    choice = int(input())
    if choice == 1:
        acount = Account(True)
        acount.print_message()
    elif choice == 2:
        print("Enter your card number:")
        card_number = input()
        pin = int(input("Enter your PIN:"))
        if account_avilable(card_number):
            cur.execute(f"""SELECT pin from card where number = {card_number}""")
            account_pin=cur.fetchone()[0]
            if str(account_pin) == str(pin):
                account=Account(False,card_number)
                account.log_in()
            else:
                print("Wrong card number or PIN!")
        else:
            print("Wrong card number or PIN!")
    elif choice == 0:
        print("Bye!")
        break

