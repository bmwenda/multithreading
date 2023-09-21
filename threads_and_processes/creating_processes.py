import multiprocessing
from multiprocessing import Process

def do_cpu_intensive_work(thread_num):
    print("Thread %s starting work..." % thread_num)
    x = 0
    for i in range(20000000):
        x += 1

    print("Thread %s finished work!" % thread_num)

def run_process():
    # by using processes, we sidestep the Global Interpretor Lock
    # thus we have parallelism thanks to multiple processes running
    multiprocessing.set_start_method("fork") # ==> default for unix
    for i in range(5):
        p = Process(target=do_cpu_intensive_work, args=(i + 1,))
        p.start()

if __name__ == "__main__":
    run_process()
