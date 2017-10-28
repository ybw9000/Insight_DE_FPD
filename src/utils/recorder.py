from .finders import medianfinder

class Recorder(object):
    def __init__(self):
        """
        Initialize a Recorder class which keeps the running median,
        total transactions, and total amout.
        """
        self.total_amt = 0
        self.total_tran = 0
        self.median = medianfinder.MedianFinder()

    def record(self, amt):
        """
        put the streamed amount into different field.
        input:
            amt: float
        """
        self.total_amt += amt
        self.total_tran += 1
        self.median.addNum(amt)

    def indicate(self):
        """
        output the median, total transactions and total amouts so far.
        returns: tuple of int
        """
        return (self.median.findMedian(), self.total_tran,
                round(self.total_amt))
