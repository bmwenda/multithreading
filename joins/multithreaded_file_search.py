"""
Searches for a filename in a given directory recursively
For each recursive call, we create a new thread
We call join on each thread to wait for it to terminate and return their results
"""

import os
from os.path import isdir, join
from threading import Lock, Thread

matches = []
mutex = Lock()

def search_file(root, filename):
    print("Searching in:", root)
    child_threads = []
    for file in os.listdir(root):
        full_path = join(root, file)
        if filename in file:
            mutex.acquire()
            matches.append(full_path)
            mutex.release()
        if isdir(full_path):
            t = Thread(target=search_file, args=([full_path, filename]))
            t.start()
            child_threads.append(t)
    for t in child_threads:
        t.join()


if __name__ == "__main__":
    parent_thread = Thread(target=search_file, args=(["../../", "Gemfile"]))
    parent_thread.start()
    parent_thread.join()
    print("Found %s matches:" % len(matches))
    for match in matches:
        print(match)
