"""
Demonstrates how semaphores use conditional variables to implement locks
and signal to other threads to react to changes in shared variable state
"""

from threading import Thread, Condition

class Account:
    balance = 1000
    cv = Condition()

    def deposit(self):
        for i in range(100000000): # high value to increase the chances of getting race conditions
            self.cv.acquire()
            self.balance += 1000
            self.cv.notify()
            self.cv.release()
        print("Done depositing")

    def withdraw(self):
        withdraw_amount = 2000
        for i in range(50000000):
            self.cv.acquire()
            while self.balance < withdraw_amount:
                self.cv.wait()
            self.balance -= withdraw_amount
            if self.balance < 0: # because we have a wait condition, this state is never reached
                print("Overdraft! ", self.balance) # never printed on console
            self.cv.release()
        print("Done withdrawing")

if __name__ == "__main__":
    account = Account()
    t1 = Thread(target=account.deposit, args=())
    t1.start()
    t2 = Thread(target=account.withdraw, args=())
    t2.start()
    t1.join()
    t2.join()
    print("Current balance: %s " % account.balance) # should be 1000
