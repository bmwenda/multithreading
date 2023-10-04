"""Queues can be used to send messages to other threads
This is an alternative paradigm from accessing shared memory directly
Instead, messages are passed via a queue between two processes/threads
where one is a producer and the other is a consumer
"""

import time
from queue import Queue
from threading import Thread

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
    q = Queue(maxsize=20)
    Thread(target=producer, args=(q,)).start()
    Thread(target=consumer, args=(q,)).start()
