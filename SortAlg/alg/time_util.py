import time

def time_execute(func):
    def function(*args):
        start = time.perf_counter()
        result = func(*args)
        end = float((time.perf_counter() - start) * 1000)
        return result, end
    return function