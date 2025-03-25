import random

import time_util

@time_util.time_execute
def radix_sort(array: list) -> list:
    maximum = max(array)
    radix = 1
    while maximum // radix > 0:
        array = sort_by_radix(array, radix)
        radix *= 10

    return array

def merge_baskets(baskets: list) -> list:
    merge_array = []

    for basket in baskets:
        merge_array.extend(basket)

    return merge_array

def sort_by_radix(array: list, radix: int) -> list:
    baskets = [[] for _ in range(10)]

    for num in array:
        index_basket = (num // radix) % 10
        baskets[index_basket].append(num)

    return merge_baskets(baskets)

print(radix_sort([random.randint(1, 1000) for _ in range(10000)]))