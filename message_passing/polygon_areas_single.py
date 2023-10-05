"""Calculates area of polygons using the shoelace formula https://en.wikipedia.org/wiki/Shoelace_formula
See ./polygon_areas_pools.py for a solution using thread pools
"""

import os
import re
import time

PTS_REGEX = "\((\d*),(\d*)\)"

def find_area(points_str):
    points = []
    area = 0.0
    for xy in re.finditer(PTS_REGEX, points_str):
        points.append((int(xy.group(1)), int(xy.group(2))))

    for i in range(len(points)):
        a, b = points[i], points[(i + 1) % len(points)]
        area += a[0] * b[1] - a[1] * b[0]
    area = abs(area) / 2.0

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "message_passing", "polygons.txt")
    f = open(path, "r")
    lines = f.read().splitlines()
    start = time.time()
    for line in lines:
        find_area(line)
    end = time.time()
    print("Time taken", end - start)
