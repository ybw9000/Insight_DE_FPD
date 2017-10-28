# Table of Contents
1. [Algorithm summary](README.md#Algorithm summary)
2. [Module summary](README.md#Module summary)
3. [Unit test](README.md#Unit test)
4. [Repo directory structure](README.md#repo-directory-structure)


# Algorithm summary

The core idea is how to efficiently query the median in a streamed data. This algorithm uses two heaps to store all the input data and each insert takes O(log(n)) time and each query takes O(1) time, as described below:

-Initialize two empty heaps ("min heap"), say `left` and `right`. `left` always has the same length of or one more element than `right`, i.e., len(left) = len(right) or len(left) = len(right) + 1. With two empty heaps, this is satisfied.

-Each time when a streamed value `num` comes in, we push it into `right` if len(left) == len(right); otherwise (len(left) == len(right) + 1) we push -`num` into `left`. Then we pop the top element `heap[0]` from that heap and push -`heap[0]` into the other heap. The negative sign just makes `left` serve as a "max heap". This way ensures that all the `num` in `left` are no greater than all the `num` in `right` as well as the above length condition. This insert takes O(log(n)).

-Since the -`left[0]` is the largest input value in `left` and `right[0]` is the smallest input value in `right`, the median is simply the average of them `(right[0] - left[0])/2` if len(left) == len(right) else -`left[0]`. This query takes O(1).

-This algorithm is wrapped in a class named "MedianFinder" in `~/src/utils/finders/medianfinder.py` along with several naive algorithms which are just for test/debug issue.

# Module summary

For this challenge, I used a `Recorder` class to wrap the above mentioned `MedianFinder` class to record the median, total transactions and total amount streamed in so far. Implementation of total transactions and total amount are trivial. This `Recorder` is under `~/src/utils/recorder.py`.

For every key (CMTE_ID, ZIP_CODE/TRANSACTION_DT), it has a corresponding "Recorder" as its value. In order to make the hierarchy easier to query, instead of using (CMTE_ID, ZIP_CODE/TRANSACTION_DT) as a key, I used two level dictionaries, i.e., defaultdict(lambda : defaultdict(Recorder)). For the first level, CMTE_ID is the key, and a corresponding dictionary is the value, for the second level, ZIP_CODE/TRANSACTION_DT is the key, and a "Recorder" is the value. So at any given time, the median, total transactions and total amount of a particular (CMTE_ID, ZIP_CODE/TRANSACTION_DT) can be queried by dictionary[CMTE_ID][ZIP_CODE/TRANSACTION_DT]. These dictionaries are wrapped in a "Streamer" class in `~/src/find_political_donors.py` or `~/src/utils/streamer.py`.

The work flow is as follows:

-For each line in the input file, determines whether it is invalid. If so, skip to the next line.

-Check if ZIP_CODE is valid. If so, dump the input value into the corresponding "Recorder", then query the median, total transactions and total amount recorded so far and write them into `medianvals_by_zip.txt`.

-Check if TRANSACTION_DT is valid. If so, dump the input value into the corresponding "Recorder".

-After the streaming is done, sort the keys (CMTE_ID) in the first level dictionary alphabetically, followed by sorting the keys (TRANSACTION_DT) in second level dictionaries chronologically. Then just query the corresponding "Recorder" of each (CMTE_ID, TRANSACTION_DT) and write the result into `medianvals_by_date.txt`.

These steps are implemented in a "Streamer" class in `~/src/find_political_donors.py` or `~/src/utils/streamer.py`. The code are exactly the same for the "Streamer" class in these two files.

# Unit test

I implemented a tester to test the "MedianFinder" works properly and survive stress test by comparing the result from the optimized "MedianFinder" to the naive/brute force algorithms. This tester can be found under `~/src/utils/medianfinder_tester.py`.

For the unit tests for the main module, I just wrote several more test cases and test the main module by the provided `~/insight_testsuite/run_tests.sh`.

My own test samples are as below:

`~/insight_testsuite/tests/my_test1`:
    -contains 8 tests, including:
    -all fields are valid
    -invalid date: 02292017
    -invalid date: Null
    -invalid zip: Null
    -invalid zip: digits less than 5
    -invalid zip: contains non-numeric char
    -invalid input: TRANSACTION_AMT Null
    -invalid input: CMTE_ID Null

`~/insight_testsuite/tests/my_test2`:
    -contains 2 tests, including:
    -invalid input: TRANSACTION_AMT Null
    -invalid input: CMTE_ID Null

# Repo directory structure

The directory structure for the repo looks like this:

    ├── README.md
    ├── run.sh
    ├── src
    │   └── find_political_donors.py
    |   └── utils
    |       └── recorder.py
    |       └── streamer.py
    |       └── medianfinder_tester.py
    |       └── finders
    |           └── medianfinder.py
    ├── input
    │   └── itcont.txt
    ├── output
    |   └── medianvals_by_zip.txt
    |   └── medianvals_by_date.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── itcont.txt
            |   |__ output
            |   │   └── medianvals_by_zip.txt
            |   |__ └── medianvals_by_date.txt
            ├── my_test1
            |   ├── input
            |   │   └── your-own-input.txt
            |   |── output
            |       └── medianvals_by_zip.txt
            |       └── medianvals_by_date.txt
            ├── my_test2
                ├── input
                │   └── your-own-input.txt
                |── output
                    └── medianvals_by_zip.txt
                    └── medianvals_by_date.txt
