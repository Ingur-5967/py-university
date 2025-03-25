import random
import unittest

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

print(radix_sort([random.randint(1, 10000) for _ in range(10000)]))

print(f"Fon n=10000: {radix_sort([random.randint(1, 10000) for _ in range(10000)])[1]}")
print(f"Fon n=50000: {radix_sort([random.randint(1, 10000) for _ in range(50000)])[1]}")
print(f"Fon n=100000: {radix_sort([random.randint(1, 10000) for _ in range(100000)])[1]}")
print(f"Fon n=1000000: {radix_sort([random.randint(1, 10000) for _ in range(1000000)])[1]}")
print(f"Fon n=5000000: {radix_sort([random.randint(1, 10000) for _ in range(5000000)])[1]}")
print(f"Fon n=10000000: {radix_sort([random.randint(1, 10000) for _ in range(10000000)])[1]}")


class RadixSortTest(unittest.TestCase):

    def test_radix_sort_equal(self):
        array = [random.randint(1, 1000) for _ in range(1000)]
        self.assertEqual(radix_sort(array)[0], sorted(array))

    def test_radix_sort_is(self):
        array = [random.randint(1, 1000) for _ in range(1000)]
        self.assertIs(radix_sort(array)[0], sorted(array))

if __name__ == '__main__':
    unittest.main()