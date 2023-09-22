
"""
Fetches resources in parallel using threads while using a lock to prevent race conditions

Note:
You need to carefully think about the best place to acquire the lock and where to release it
There is a balancing act between:
    - preventing race conditions while also not blocking threads unnecesarrily
    - avoiding calling acquire() multiple times, e.g in a loop as this is an expensive operation
This differs on a case by case basis, your context may vary
In this example, more time is spent making external API requests, so that's where threads are useful
Acquiring a lock before we write to the hash in a loop would be expensive and is the slower option here
This is the correct tradeoff to make in this specific scenario
"""

import json
import time
from threading import Thread, Lock
import urllib.request

threads_count = 0 # shared memory
LETTERS = "abcdefghijklmnopqrstuvxyz"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0"}

def frequency_counter(url, hash, mutex):
    req = urllib.request.Request(url, headers=HEADERS)
    response = urllib.request.urlopen(req)
    txt = str(response.read())
    letters = [l for l in txt.lower()]

    mutex.acquire() # Blocking threads here is better than calling acquire() n = letters.length times
    for char in letters:
        if char in hash.keys():
            hash[char] += 1

    global threads_count
    threads_count += 1
    mutex.release()


def run_counter():
    frequency = {}
    mutex = Lock()
    for letter in LETTERS:
        frequency[letter] = 0

    start = time.time()
    for i in range(5000, 5050):
        url = f"https://www.rfc-editor.org/rfc/rfc{i}.txt"
        t = Thread(target=frequency_counter, args=(url, frequency, mutex,))
        t.start()

    while True:
        mutex.acquire()
        if threads_count == 50:
            break
        mutex.release()
        time.sleep(0.5)

    end = time.time()
    sorted_frequency = dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True))
    print(f"Finished in {end - start} seconds")
    print(json.dumps(sorted_frequency, indent=4))

if __name__ == "__main__":
    run_counter()
