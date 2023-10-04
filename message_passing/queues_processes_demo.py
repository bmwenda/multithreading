"""Queues can be used to send messages to other processes
This is an alternative paradigm from accessing shared memory directly
Instead, messages are passed via a queue between two processes
where one is a producer and the other is a consumer
"""

import time
import multiprocessing
from multiprocessing import Process, Queue

def consumer(q):
    """q implements a get() method to read messages"""
    while True:
        msg = q.get()
        print(f"{msg}: well received!")
        time.sleep(1)

def producer(q):
    """q implements a put() method to add messages to the queue"""
    while(True):
        q.put("receive my greetings")
        print("Message sent!")


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    q = Queue(maxsize=20)
    Process(target=producer, args=(q,)).start()
    Process(target=consumer, args=(q,)).start()
