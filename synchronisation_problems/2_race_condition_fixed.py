"""
Using a mutex, we can acquire a lock before writing to a shared variable
This fixes the race condition and the code is now thread safe
"""

import time
from threading import Thread, Lock

class Account:
    def __init__(self):
        self.balance = 1000
        self.mutex = Lock()

    def deposit(self):
        for i in range(10000000): # high value to increase the chances of getting race conditions
            self.mutex.acquire()
            self.balance += 1000
            self.mutex.release()
        print("Done depositing")

    def withdraw(self):
        for i in range(10000000):
            self.mutex.acquire()
            self.balance -= 1000
            self.mutex.release()
        print("Done withdrawing")

if __name__ == "__main__":
    account = Account()
    Thread(target=account.deposit, args=()).start()
    Thread(target=account.withdraw, args=()).start()
    time.sleep(10) # allow threads to finish before reading balance
    print("Current balance: %s " % account.balance) # should be 1000
