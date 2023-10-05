"""Uses pipes to extracts weather data from metar (meteriological aerodrome report) files and calculates wind direction
Extends the single process solution in ./wind_direction_single.py
Steps are sequential and each step receives data from a pipe, does it's calculations and
passes the data to the next function through a pipe
Steps:
    - read metar files
    - parse
    - extract wind direction
    - mine wind distributions
"""

import os
import re
from os.path import join

import time
import multiprocessing
from multiprocessing import Pipe
from multiprocessing.context import Process

WIND_REGEX = "\d* METAR.*EGLL \d*Z [A-Z ]*(\d{5}KT|VRB\d{2}KT).*="
WIND_EX_REGEX = "(\d{5}KT|VRB\d{2}KT)"
VARIABLE_WIND_REGEX = ".*VRB\d{2}KT"
VALID_WIND_REGEX = "\d{5}KT"
WIND_DIR_ONLY_REGEX = "(\d{3})\d{2}KT"
TAF_REGEX = ".*TAF.*"
COMMENT_REGEX = "\w*#.*"
METAR_CLOSE_REGEX = ".*="


def parse_to_array(text_conn_b, metars_conn_a):
    text = text_conn_b.recv()
    while text is not None:
        lines = text.splitlines()
        metar_str = ""
        metars = []
        for line in lines:
            if re.search(TAF_REGEX, line):
                break
            if not re.search(COMMENT_REGEX, line):
                metar_str += line.strip()
            if re.search(METAR_CLOSE_REGEX, line):
                metars.append(metar_str)
                metar_str = ""
        metars_conn_a.send(metars)
        text = text_conn_b.recv()
    metars_conn_a.send(None)


def extract_wind_direction(metars_conn_b, winds_conn_a):
    metars = metars_conn_b.recv()
    while metars is not None:
        winds = []
        for metar in metars:
            if re.search(WIND_REGEX, metar):
                for token in metar.split():
                    if re.match(WIND_EX_REGEX, token):
                        winds.append(re.match(WIND_EX_REGEX, token).group(1))
        winds_conn_a.send(winds)
        metars = metars_conn_b.recv()
    winds_conn_a.send(None)


def mine_wind_distribution(winds_conn_b, dist_conn_a):
    wind_dist = [0] * 8
    winds = winds_conn_b.recv()
    while winds is not None:
        for wind in winds:
            if re.search(VARIABLE_WIND_REGEX, wind):
                for i in range(8):
                    wind_dist[i] += 1
            elif re.search(VALID_WIND_REGEX, wind):
                d = int(re.match(WIND_DIR_ONLY_REGEX, wind).group(1))
                dir_index = round(d / 45.0) % 8
                wind_dist[dir_index] += 1
        winds = winds_conn_b.recv()
    dist_conn_a.send(wind_dist)


if __name__ == '__main__':
    current_path = os.path.dirname(os.path.realpath(__file__))
    path_with_files = join(current_path, "../metarfiles")

    text_conn_a, text_conn_b = Pipe()
    metars_conn_a, metars_conn_b = Pipe()
    winds_conn_a, winds_conn_b = Pipe()
    dist_conn_a, dist_conn_b = Pipe()

    Process(target=parse_to_array, args=(text_conn_b, metars_conn_a,)).start()
    Process(target=extract_wind_direction, args=(metars_conn_b, winds_conn_a,)).start()
    Process(target=mine_wind_distribution, args=(winds_conn_b, dist_conn_a,)).start()

    start = time.time()
    for file in os.listdir(path_with_files):
        f = open(join(path_with_files, file), "r")
        text = f.read()
        text_conn_a.send(text)
    text_conn_a.send(None)
    wind_dist = dist_conn_b.recv()
    end = time.time()
    print(wind_dist)
    print("Time taken", end - start)
