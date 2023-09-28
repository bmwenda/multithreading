"""Basic demo of multithreading"""

import os
import time
import threading
from threading import Thread

def do_work():
    thread_id = threading.current_thread().ident
    print("Thread %s starting work..." % thread_id)
    time.sleep(1)
    print("Thread %s finished work!" % thread_id)

def do_cpu_intensive_work():
    thread_id = threading.current_thread().ident
    print("Thread %s starting work..." % thread_id)
    x = 0
    # add a cpu intensive operation to show effect of GIL https://en.wikipedia.org/wiki/Global_interpreter_lock
    # benefit of multithreading is lost
    for i in range(20000000):
        x += 1
    print("Thread %s finished work!" % thread_id)


def run_do_work():
    for i in range(5):
        t = Thread(target=do_work, args=())
        t.start()

def run_cpu_intensive_work():
    for i in range(5):
        t = Thread(target=do_cpu_intensive_work, args=())
        t.start()

if __name__ == '__main__':
    # run_do_work()
    run_cpu_intensive_work()
