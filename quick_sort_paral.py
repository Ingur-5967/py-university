import random
import threading
import time


def quick_sort(array: list, parallel_sort: bool = False, num_threads: int = 1, array_size: int = 0) -> list:
    if len(array) <= 1:
        return array

    pivot = array[len(array) // 2]
    left = [x for x in array if x < pivot]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if x > pivot]

    if parallel_sort:
        results = [None] * 2

        def sort_left():
            results[0] = quick_sort(left, parallel_sort, num_threads // 2)

        def sort_right():
            results[1] = quick_sort(right, parallel_sort, num_threads // 2)

        if len(array) > array_size and num_threads > 0:
            left_thread = threading.Thread(target=sort_left)
            right_thread = threading.Thread(target=sort_right)

            left_thread.start()
            right_thread.start()

            left_thread.join()
            right_thread.join()

            sorted_left = results[0]
            sorted_right = results[1]
        else:
            sorted_left = quick_sort(left, False, num_threads)
            sorted_right = quick_sort(right, False, num_threads)

        return sorted_left + middle + sorted_right
    else:
        return quick_sort(left) + middle + quick_sort(right)

def search_result(container, element_count, thread_count=None):
    for info in container:
        if info[0] == element_count:
            if thread_count is None: return info[-1]
            else:
                if info[1] != thread_count: continue
                return info[-1]


array_100 = [random.randint(1, 10000) for _ in range(100)]
array_1000 = [random.randint(1, 10000) for _ in range(1000)]
array_10000 = [random.randint(1, 10000) for _ in range(10000)]
array_100000 = [random.randint(1, 10000) for _ in range(100000)]
array_1000000 = [random.randint(1, 10000) for _ in range(1000000)]
array_10000000 = [random.randint(1, 10000) for _ in range(1000000)]

data = [array_100, array_1000, array_100000, array_1000000, array_1000000]

print("Замеры для обычной сортировки (без Паралл.)")
default_timing = list(tuple[int, int, float]())
for array in data:
    start = time.time()
    quick_sort(array, False, array_size=1000)
    end = float((time.time() - start) / 1000)

    default_timing.append((len(array), 1000, end))
print(f"default timing: {default_timing}")

print("Замеры для сортировки (2 thread Паралл.)")
parallel_timing_2 = list(tuple[int, int, int, float]())
for array in data:
    start = time.time()
    quick_sort(array, True, 2, 1000)
    end = float((time.time() - start) / 1000)

    parallel_timing_2.append((len(array), 2, 1000, end))
print(f"2 thread: {parallel_timing_2}")

print("Замеры для сортировки (4 thread Паралл.)")
parallel_timing_4 = list(tuple[int, int, int, float]())
for array in data:
    start = time.time()
    quick_sort(array, True, 4, 1000)
    end = float((time.time() - start) / 1000)

    parallel_timing_4.append((len(array), 4, 1000, end))

print(f"4 thread: {parallel_timing_4}")

print("Замеры для сортировки (8 thread Паралл.)")
parallel_timing_8 = list(tuple[int, int, float]())
for array in data:
    start = time.time()
    quick_sort(array, True, 8, 1000)
    end = float((time.time() - start) / 1000)

    parallel_timing_8.append((len(array), 8, 1000, end))

print(f"8 thread: {parallel_timing_8}")

stat = list[tuple[int, int]]()
for statistic in data:
    size = len(statistic)

    for container in [parallel_timing_2, parallel_timing_4, parallel_timing_8]:
        for thread_count in [2, 4, 8]:
            for_default_timing = search_result(default_timing, size)
            for_parallel_timing = search_result(container, size, thread_count)

            if for_parallel_timing is None: continue

            speedup = for_default_timing / for_parallel_timing

            stat.append((size, speedup))

print(stat)
