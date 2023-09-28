import multiprocessing
from multiprocessing import Process
import os

def do_cpu_intensive_work():
    print("Process %s starting work! " % os.getpid())
    x = 0
    for i in range(20000000):
        x += 1
    print("Process %s finished work!" % os.getpid())

def run_process():
    # by using processes, we sidestep the Global Interpretor Lock
    # thus we have parallelism thanks to multiple processes running
    multiprocessing.set_start_method("fork") # ==> default for unix
    for i in range(5):
        p = Process(target=do_cpu_intensive_work, args=())
        p.start()

if __name__ == "__main__":
    print("Parent process id:", os.getpid())
    run_process()
