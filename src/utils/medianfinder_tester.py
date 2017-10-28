import unittest
from finders import medianfinder
import random

class Tester(unittest.TestCase):

    def test_one_num(self):
        mf = medianfinder.MedianFinder()
        mf.addNum(1)
        self.assertEqual(1, mf.findMedian())

    def test_two_num_ceil(self):
        mf = medianfinder.MedianFinder()
        mf.addNum(1)
        mf.addNum(2)
        self.assertEqual(2, mf.findMedian())

    def test_two_num_floor(self):
        mf = medianfinder.MedianFinder()
        mf.addNum(0)
        mf.addNum(0.9)
        self.assertEqual(0, mf.findMedian())

    def test_stress_float(self):
        mf = medianfinder.MedianFinder()
        mf_b = medianfinder.BisectMedianFinder()
        for i in range(100):
            for j in range(1000):
                num = random.random()*1e6
                mf.addNum(num)
                mf_b.addNum(num)
            self.assertEqual(mf.findMedian(), mf_b.findMedian())

    def test_stress_int(self):
        mf = medianfinder.MedianFinder()
        mf_b = medianfinder.BisectMedianFinder()
        for i in range(100):
            for j in range(1000):
                num = random.randint(0, 1e6)
                mf.addNum(num)
                mf_b.addNum(num)
            self.assertEqual(mf.findMedian(), mf_b.findMedian())

if __name__ == '__main__':
    unittest.main()
