import time

class Timer:
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        if self.start_time is None:
            raise RuntimeError("Timer was not started.")

        return round(
            time.perf_counter() - self.start_time,
            3
        )