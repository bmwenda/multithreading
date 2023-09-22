
"""
Demonstrates multithreading by fetching multiple documents and counting letter frequency
The results are inconsistent if the code is executed multiple times
This is because we are using shared memory (threads_count)
This causes synchronisation issues hence the inconsistent results
"""

import json
import time
from threading import Thread
import urllib.request

threads_count = 0 # shared memory ==> incosistent results!
LETTERS = "abcdefghijklmnopqrstuvxyz"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0"}

def frequency_counter(url, hash):
    req = urllib.request.Request(url, headers=HEADERS)
    response = urllib.request.urlopen(req)
    txt = str(response.read())
    letters = [l for l in txt.lower()]

    for char in letters:
        if char in hash.keys():
            hash[char] += 1

    global threads_count
    threads_count += 1


def run_counter():
    frequency = {}
    for letter in LETTERS:
        frequency[letter] = 0

    start = time.time()
    for i in range(5000, 5050):
        url = f"https://www.rfc-editor.org/rfc/rfc{i}.txt"
        t = Thread(target=frequency_counter, args=(url, frequency,))
        t.start()

    while threads_count < 50:
        time.sleep(0.5)

    end = time.time()
    sorted_frequency = dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True))
    print(f"Finished in {end - start} seconds")
    print(json.dumps(sorted_frequency, indent=4))

if __name__ == "__main__":
    run_counter()
