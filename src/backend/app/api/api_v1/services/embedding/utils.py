import time
from contextlib import contextmanager

@contextmanager
def timer():
    start_time = time.time()
    yield
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")


class Timer:
    def __init__(self, context_name: str = ''):
        self.start_time = None
        self.end_time = None 
        self.elapsed_time = None
        self.context_name = context_name

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        msg =   (f"{self.context_name} took {self.elapsed_time:.4f} seconds") if self.context_name else  (f"Time Taken: {self.elapsed_time:.4f} seconds") 
        print(msg )
        
    def elapsed(self):
        return self.elapsed_time