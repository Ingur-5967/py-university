import random
import unittest

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

print(f"Fon n=1000: {bubble_sort([random.randint(1, 10000) for _ in range(1000)])[1]}")
print(f"Fon n=10000: {bubble_sort([random.randint(1, 10000) for _ in range(10000)])[1]}")
print(f"Fon n=25000: {bubble_sort([random.randint(1, 10000) for _ in range(25000)])[1]}")
print(f"Fon n=40000: {bubble_sort([random.randint(1, 10000) for _ in range(40000)])[1]}")
print(f"Fon n=50000: {bubble_sort([random.randint(1, 10000) for _ in range(50000)])[1]}")

class BubbleSortTest(unittest.TestCase):

    def test_bubble_sort_equal(self):
        array = [random.randint(1, 1000) for _ in range(1000)]
        self.assertEqual(bubble_sort(array)[0], sorted(array))

    def test_bubble_sort_is(self):
        array = [random.randint(1, 1000) for _ in range(1000)]
        self.assertIs(bubble_sort(array)[0], sorted(array))

if __name__ == '__main__':
    unittest.main()