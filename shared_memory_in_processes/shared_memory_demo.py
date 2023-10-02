"""Demonstrates that processes do not share memory directly
Techniques such as message passing are used to share memory resources
"""

import time
import multiprocessing
from multiprocessing.context import Process

def print_array(array):
    for _ in range(len(array) * 2):
        print(*array, sep=", ")
        time.sleep(1)

if __name__ == "__main__":
    # shared aray using multiprocessing module allows both processes to access the object
    shared_arr = multiprocessing.Array('i', [-1] * 10)
    p = Process(target=print_array, args=(shared_arr,))
    p.start()
    for j in range(10):
        time.sleep(2)
        for i in range(10):
            shared_arr[i] = j
