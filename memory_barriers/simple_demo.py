"""Demonstrate the concept of memory barriers"""

import time
from threading import Barrier, Thread

barrier = Barrier(2)

def wait_on_barrier(thread_name, time_to_sleep):
    """After both threads call wait() the lock is released
    Thread 1 waits for thread 2 to wake up, which then immediately calls wait()
    The wait is released and the two threads start simultaneously in the next iteration
    """
    for i in range(5):
        print(thread_name, "running...")
        time.sleep(time_to_sleep)
        print(thread_name, "is waiting on barrier")
        barrier.wait()

    print(thread_name, "is done!")

if __name__ == "__main__":
    thread1 = Thread(target=wait_on_barrier, args=("Thread 1", 2))
    thread2 = Thread(target=wait_on_barrier, args=("Thread 2", 5))
    thread1.start()
    thread2.start()
