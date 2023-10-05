"""Demonstration of message passing with a duplex(bidirectional) pipe
"""

import time
import multiprocessing
from multiprocessing import Process, Pipe

def consumer(pipe_conn):
    while True:
        msg = pipe_conn.recv()
        print("Consumer received:", msg)
        time.sleep(1)
        greeting = f"Hello from consumer at, {time.time()}"
        pipe_conn.send(greeting)
        print("Consumer sent:", greeting)

def producer(pipe_conn):
    while(True):
        greeting = f"Hello from producer at, {time.time()}"
        pipe_conn.send(greeting)
        print("Producer sent:", greeting)
        msg = pipe_conn.recv()
        print("Producer received:", msg)
        time.sleep(1)


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    pipe_conn_a, pipe_conn_b = Pipe(duplex=True) # Pipe() returns a tuple of Connection objects
    Process(target=producer, args=(pipe_conn_a,)).start()
    Process(target=consumer, args=(pipe_conn_b,)).start()
