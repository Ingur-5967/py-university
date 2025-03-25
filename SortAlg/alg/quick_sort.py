import random


import time_util

@time_util.time_execute
def quick_sort(array: list) -> tuple[list, float] | list:
    if len(array) <= 1:
        return array
    pivot = array[len(array) // 2]
    left = [x for x in array if x < pivot]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if x > pivot]
    return quick_sort(left)[0] + middle + quick_sort(right)[0]

print(quick_sort([random.randint(1, 10000) for _ in range(10000)]))