import time

def time_execute(func):
    def function(*args):
        start = time.time()
        result = func(*args)
        return result, time.time() - start
    return function