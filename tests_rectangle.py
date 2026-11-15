import unittest
import rectangle

class RectangleTestCase(unittest.TestCase):
    #simple tests
    def test_square(self):
        result = rectangle.sq(5, 3)
        self.assertEqual(result, 15)
    def test_perimetr(self):
        result = rectangle.pr(5, 3)
        self.assertEqual(result, 16)
    #same sides test
    def test_same_sides_square(self):
        result = rectangle.sq(10, 10)
        self.assertEqual(result, 100)
    def test_same_sides_perimetr(self):
        result = rectangle.pr(10, 10)
        self.assertEqual(result, 40)
    #0 sq & 0 pr
    def test_zero_square(self):
        result = rectangle.sq(10, 0)
        self.assertEqual(result, 0)
    def test_zero_perimetr(self):
        result = rectangle.pr(10, 0)
        self.assertEqual(result, 20)
    #not int test
    def test_float_square(self):
        result = rectangle.sq(2.5, 4)
        self.assertAlmostEqual(result, 10)
    def test_float_perimetr(self):
        result = rectangle.pr(2.5, 4)
        self.assertAlmostEqual(result, 13)
    #simple swap values test
    def test_swap_square(self):
        result = rectangle.sq(3, 5)
        self.assertEqual(result, 15)
    def test_swap_perimetr(self):
        result = rectangle.pr(3, 5)
        self.assertEqual(result, 16)
    # negative values test
    def test_negative_square(self):
        self.assertRaises(ValueError, rectangle.sq, -5, 3)
    def test_negative_perimetr(self):
        self.assertRaises(ValueError, rectangle.pr, -5, 3)
if __name__ == "__main__":
    unittest.main()