import random

import time_util

@time_util.time_execute
def bubble_sort(array: list) -> list:
    n = len(array)
    for i in range(0, n - 1):
        for j in range(0, n - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]

    return array

print(bubble_sort([random.randint(1, 10000) for _ in range(10000)]))