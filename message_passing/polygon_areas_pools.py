"""Calculates area of polygons using the shoelace formula https://en.wikipedia.org/wiki/Shoelace_formula
Implements message passing using a queue and process pools
    - a master process receives a request from a client
    - request is added to a queue
    - a worker threads listening to the queue picks the message if it is idle
    - if no process is idle, master process responds to the client that all resources are busy
"""

import os
import re
import time
from multiprocessing import Process, Queue

PTS_REGEX = "\((\d*),(\d*)\)"
PROCESS_COUNT = 2

def find_area(queue):
    points_str = queue.get()
    while points_str is not None:
        points = []
        area = 0.0
        for xy in re.finditer(PTS_REGEX, points_str):
            points.append((int(xy.group(1)), int(xy.group(2))))

        for i in range(len(points)):
            a, b = points[i], points[(i + 1) % len(points)]
            area += a[0] * b[1] - a[1] * b[0]
        area = abs(area) / 2.0
        points_str = queue.get()

if __name__ == "__main__":
    q = Queue(maxsize=1000)
    processes = []
    for _ in range(PROCESS_COUNT):
        p = Process(target=find_area, args=(q,))
        processes.append(p)
        p.start()

    path = os.path.join(os.getcwd(), "message_passing", "polygons.txt")
    f = open(path, "r")
    lines = f.read().splitlines()

    start = time.time()
    for line in lines:
        q.put(line)
    for _ in range(PROCESS_COUNT): q.put(None) # mark end of queue for all processes
    for process in processes: process.join() # wait for all processes to finish
    end = time.time()
    print("Time taken", end - start)
