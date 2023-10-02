"""Matrix multiplation using multiprocessing
Each process will compute each row, and move to the next row offset
e.g given two cores, a process will compute rows n where n = cores + row_index
See memory_barriers/matrix_multiplication_multithreaded.py for multithreaded solution
"""

import time
from random import randint
import multiprocessing
from multiprocessing.context import Process

N = 200 # reasonable number to observe run time
PROCESS_COUNT = 2 # Logical cores in cpu

def initiliaze_matrices(matrix_a, matrix_b):
    for matrix in [matrix_a, matrix_b]:
        for row in range(N):
            for col in range(N):
                matrix[(row * N) + col] = randint(-10, 10)

def row_multiplication(processId, matrix_a, matrix_b, result, work_start, work_complete):
    while True:
        work_start.wait()
        for row in range(processId, N, PROCESS_COUNT):
            for col in range(N):
                for i in range(N):
                    result[(row * N) + col] += matrix_a[(row * N) + i] * matrix_b[(row * N) + col]
        work_complete.wait() # each process waits at second barrier after completion

if __name__ == "__main__":
    multiprocessing.set_start_method('fork')
    matrix_a = multiprocessing.Array('i', [0] * (N * N), lock=False)
    matrix_b = multiprocessing.Array('i', [0] * (N * N), lock=False)
    result = multiprocessing.Array('i', [0] * (N * N), lock=False)

    work_start = multiprocessing.Barrier(PROCESS_COUNT + 1) # +1 accounts for parent process
    work_complete = multiprocessing.Barrier(PROCESS_COUNT + 1)

    for process in range(PROCESS_COUNT):
        Process(target=row_multiplication, args=(process, matrix_a, matrix_b, result, work_start, work_complete)).start()

    start_time = time.time()
    for i in range(10):
        initiliaze_matrices(matrix_a, matrix_b)
        for i in range(N * N):
            result[i] = 0
        work_start.wait() # main process calls wait and this unlocks the other process to do calculation
        work_complete.wait() # main process waits at second barrier. When the other N process reach here, lock is released and next iteration can run
    end_time = time.time()
    print("Finished in", end_time - start_time)
