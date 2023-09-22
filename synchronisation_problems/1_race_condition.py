"""
Demonstrates a race condition where two threads write to the same shared memory
Two threads perform operations that should result to the value remaining the same
However, the final value is wrong and inconsistent per run
"""

import time
from threading import Thread

class Account:
    balance = 1000

    def deposit(self):
        for i in range(100000000): # high value to increase the chances of getting race conditions
            self.balance += 1000
        print("Done depositing")

    def withdraw(self):
        for i in range(100000000):
            self.balance -= 1000
        print("Done withdrawing")

if __name__ == "__main__":
    account = Account()
    Thread(target=account.deposit, args=()).start()
    Thread(target=account.withdraw, args=()).start()
    time.sleep(10) # allow threads to finish before reading balance
    print("Current balance: %s " % account.balance) # should be 1000
