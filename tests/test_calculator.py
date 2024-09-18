import unittest

from src.calculator import sum
from src.calculator import substract
from src.calculator import multiply
from src.calculator import divide

class CalculatorTest(unittest.TestCase):

    def test_sum(self):
        assert sum(2, 3) == 5

    def test_substract(self):
        assert substract(10, 5) == 5

    def test_mult(self):
        assert multiply(3, 5) == 15

    def test_division(self):
        assert divide(30, 2) == 15        

    def test_div_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(3, 0)