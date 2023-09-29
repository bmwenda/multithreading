"""Matrix multiplation with one thread
Run time is O(n^3) hence cpu expensive
"""

from random import randint
import time

N = 200 # reasonable number to observe run time
matrix_a = [[0] * N for a in range(N)]
matrix_b = [[0] * N for b in range(N)]
result = [[0] * N for r in range(N)]

def initiliaze_matrices():
    for matrix in [matrix_a, matrix_b]:
        for row in range(N):
            for col in range(N):
                matrix[row][col] = randint(-10, 10)

def multiply():
    for row in range(N):
        for col in range(N):
            for i in range(N):
                result[row][col] += matrix_a[row][i] * matrix_b[i][col]
    print(*result, sep="\n")

if __name__ == "__main__":
    start_time = time.time()
    for i in range(10):
        initiliaze_matrices()
        result = [[0] * N for r in range(N)]
        multiply()
    end_time = time.time()
    print("Finished in", end_time - start_time)
