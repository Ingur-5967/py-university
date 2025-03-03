import unittest

import numpy as np

def simpson_rule(f, a, b, n):
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    x = np.linspace(a, b, n+1)
    fx = f(x)

    integral = (h / 3) * (fx[0] + 4 * sum(fx[1:-1:2]) + 2 * sum(fx[2:-2:2]) + fx[-1])
    return integral

f1 = lambda x: x**3 - 12*x**2 + 4
f2 = lambda x: -x**3 + x**2 - 4

def calculate_for_functions(n):
    result_for_f1 = simpson_rule(f1, 3, 6, n)
    result_for_f2 = simpson_rule(f2, 3, 6, n)
    return result_for_f2 - result_for_f1

for n in range(1, 1000000, 100000):
    print(f"Площадь фигуры для {n}: " + str(calculate_for_functions(n)))

class TestingFunctions(unittest.TestCase):

    def test_calculate_for_100_500(self):
        self.assertAlmostEqual(calculate_for_functions(100), calculate_for_functions(500))

    def test_calculate_for_100_1000(self):
        self.assertAlmostEqual(calculate_for_functions(100), calculate_for_functions(1000))

    def test_calculate_for_500_1000(self):
        self.assertAlmostEqual(calculate_for_functions(500), calculate_for_functions(1000))

    def test_calculate_for_1000_10000(self):
        self.assertAlmostEqual(calculate_for_functions(1000), calculate_for_functions(10000))

    def test_calculate_for_1000_1000000(self):
        self.assertAlmostEqual(calculate_for_functions(1000), calculate_for_functions(1000000))

    def test_calculate_for_1000_10000000(self):
        self.assertAlmostEqual(calculate_for_functions(1000), calculate_for_functions(10000000))

    def test_calculate_for_10000_10000000(self):
        self.assertAlmostEqual(calculate_for_functions(10000), calculate_for_functions(10000000))

if __name__ == "__main__":
    unittest.main()