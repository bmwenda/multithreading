"""Utilising the WaitGroup class to simplify joins
Simplifies the file search module in joins/multithreaded_file_file_search.py
"""

import os
from os.path import isdir, join
from threading import Lock, Thread
from wait_group import WaitGroup

matches = []
mutex = Lock()

def file_search(root, filename, wait_group):
    print("Searching in:", root)
    for file in os.listdir(root):
        full_path = join(root, file)
        if filename in file:
            mutex.acquire()
            matches.append(full_path)
            mutex.release()
        if isdir(full_path):
            wait_group.add(1)
            t = Thread(target=file_search, args=([full_path, filename, wait_group]))
            t.start()
    wait_group.done()


if __name__ == "__main__":
    wait_group = WaitGroup()
    wait_group.add(1)
    t = Thread(target=file_search, args=(["../../", "README.md", wait_group]))
    t.start()
    wait_group.wait()
    for match in matches:
        print(match)
