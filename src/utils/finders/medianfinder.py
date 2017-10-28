import heapq
import bisect

class MedianFinder(object):
    def __init__(self):
        """
        Initialize two heaps.
        left: list(heap) containing all the values <= median.
              left has the same length of or one more element than right.
        right: list(heap) containing all the values >= median
        Works in O(nlog(n)). Used in implementation.
        """
        self.left, self.right = [], []

    def addNum(self, num):
        """
        Put the input num into either left or right heap and moves the largest val in left to right
        or the smallest val in right to left. This makes sure left <= right.
        input:
            num: int
        returns:
            void
        """
        num = float(num)
        if len(self.left) == len(self.right):
            heapq.heappush(self.left, -heapq.heappushpop(self.right, num))
        else:
            heapq.heappush(self.right, -heapq.heappushpop(self.left, -num))

    def findMedian(self):
        """
        :rtype: int
        """
        if len(self.left) == len(self.right):
            return round((self.right[0] - self.left[0])/2)
        else:
            return round(-self.left[0])

class NaiveMedianFinder(object):
    def __init__(self):
        """
        Initialize a list to store all the input values.
        Works in O(n^2log(n)). For test only.
        """
        self.container = []

    def addNum(self, num):
        """
        put streamed in num into the list and sort it.
        input:
            num: int
        returns:
            void
        """
        num = float(num)
        self.container.append(num)
        self.container.sort()

    def findMedian(self):
        """
        return the median.
        :rtype: int
        """
        n = len(self.container)
        return round((self.container[(n - 1)//2] + self.container[n//2])/2)

class BisectMedianFinder(object):
    def __init__(self):
        """
        Initialize a list to store all the input values.
        Works in O(n^2). For test only.
        """
        self.container = []

    def addNum(self, num):
        """
        insert streamed in num into the list and keep it sorted.
        input:
            num: int
        returns:
            void
        """
        num = float(num)
        bisect.insort(self.container, num)

    def findMedian(self):
        """
        return the median.
        :rtype: int
        """
        n = len(self.container)
        return round((self.container[(n - 1)//2] + self.container[n//2])/2)
