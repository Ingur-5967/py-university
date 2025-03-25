import random
import unittest

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

print(f"Fon n=10000: {quick_sort([random.randint(1, 10000) for _ in range(10000)])[1]}")
print(f"Fon n=50000: {quick_sort([random.randint(1, 10000) for _ in range(50000)])[1]}")
print(f"Fon n=100000: {quick_sort([random.randint(1, 10000) for _ in range(100000)])[1]}")
print(f"Fon n=1000000: {quick_sort([random.randint(1, 10000) for _ in range(1000000)])[1]}")
print(f"Fon n=5000000: {quick_sort([random.randint(1, 10000) for _ in range(5000000)])[1]}")
print(f"Fon n=10000000: {quick_sort([random.randint(1, 10000) for _ in range(10000000)])[1]}")

class QuickSortTest(unittest.TestCase):

    def test_quick_sort_equal(self):
        array = [random.randint(1, 1000) for _ in range(1000)]
        self.assertEqual(quick_sort(array)[0], sorted(array))

    def test_quick_sort_is(self):
        array = [random.randint(1, 1000) for _ in range(1000)]
        self.assertIs(quick_sort(array)[0], sorted(array))

if __name__ == '__main__':
    unittest.main()