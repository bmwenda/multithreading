from threading import Condition
class WaitGroup:
    """Takes advantage of conditional variables to make convenience methods"""
    wait_count = 0
    cv = Condition()

    def add(self, count):
        self.cv.acquire()
        self.wait_count += count
        self.cv.release()

    def done(self):
        self.cv.acquire()
        if self.wait_count > 0:
            self.wait_count -= 1
        if self.wait_count == 0:
            self.cv.notify_all()
        self.cv.acquire()

    def wait(self):
        self.cv.acquire()
        while self.wait_count > 0:
            self.cv.wait()
        self.cv.acquire()
