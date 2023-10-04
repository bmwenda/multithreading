"""Pipes can be bidirectional where messages can be sent or received by each process
"""

import time
import multiprocessing
from multiprocessing import Process, Pipe

def consumer(pipe):
    while True:
        msg = pipe.recv()
        print("Consumer received:", msg)
        time.sleep(1)
        pipe.send(["Hello from consumer at", time.time()])

def producer(pipe):
    while(True):
        pipe.send(["Hello from producer at", time.time()])
        msg = pipe.recv()
        print("Producer received:", msg)
        time.sleep(1)


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    pipe_end_a, pipe_end_b = Pipe() # Pipe() returns a tuple
    Process(target=producer, args=(pipe_end_a,)).start()
