import time
from threading import Thread

def do_work(thread_num):
    print("Thread %s starting work..." % thread_num)
    time.sleep(1)
    print("Thread %s finished work!" % thread_num)

def do_cpu_intensive_work(thread_num):
    print("Thread %s starting work..." % thread_num)
    x = 0
    # add a cpu intensive operation to show effect of GIL https://en.wikipedia.org/wiki/Global_interpreter_lock
    # benefit of multithreading is lost
    for i in range(20000000):
        x += 1

    print("Thread %s finished work!" % thread_num)


def run_do_work():
    for i in range(5):
        t = Thread(target=do_work, args=[i + 1])
        t.start()

def run_cpu_intensive_work():
    for i in range(5):
        t = Thread(target=do_cpu_intensive_work, args=[i + 1])
        t.start()

if __name__ == '__main__':
    run_cpu_intensive_work()
