"""Simple demo of a deadlock situation using two threads
Two threads acquire the same locks and after some time, they hit a deadlock
"""

import time
from threading import Thread, Lock

def thread_1(lock1, lock2):
    while True:
        print("Thread 1 acquiring lock 1...")
        lock1.acquire()
        print("Thread 1 acquiring lock 2")
        lock2.acquire()
        print("Thread 1 holding lock 1 and lock 2")
        lock1.release()
        lock2.release()
        print("Thread 1: All Locks released")
        time.sleep(0.5)

def thread_2(lock1, lock2):
    while True:
        print("Thread 2 acquiring lock 2...")
        lock2.acquire()
        print("Thread 2 acquiring lock 1")
        lock1.acquire()
        print("Thread 2 holding lock 1 and lock 2")
        lock2.release()
        lock1.release()
        print("Thread 2: All Locks released")
        time.sleep(0.5)

if __name__ == "__main__":
    lock1 = Lock()
    lock2 = Lock()
    Thread(target=thread_1, args=(lock1, lock2)).start()
    Thread(target=thread_2, args=(lock1, lock2)).start()
