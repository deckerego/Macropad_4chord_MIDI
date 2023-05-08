from executionqueue import ExecutionQueue
import unittest
import time

class TestNoDelay(unittest.TestCase):

    def test_default_submit(self):
        queue = ExecutionQueue()
        queue.submit(lambda: "Default Submit")
        task = queue.next()
        self.assertEquals(task(), "Default Submit")

    def test_delay_submit(self):
        queue = ExecutionQueue()
        queue.submit(lambda: "Delayed Submit", 0.25)
        self.assertEquals(queue.next(), None)

        time.sleep(0.25)
        task = queue.next()
        self.assertTrue(task(), "Delayed Submit")

    def test_execute_order(self):
        queue = ExecutionQueue()
        queue.submit(lambda: "One")
        queue.submit(lambda: "Two")
        queue.submit(lambda: "Three")
        queue.submit(lambda: "Four")
        queue.submit(lambda: "Five")

        self.assertTrue(queue.next()(), "One")
        self.assertTrue(queue.next()(), "Two")
        self.assertTrue(queue.next()(), "Three")
        self.assertTrue(queue.next()(), "Four")
        self.assertTrue(queue.next()(), "Five")

    def test_execute_remove(self):
        queue = ExecutionQueue()
        queue.submit(lambda: "One")
        queue.submit(lambda: "Two")
        self.assertTrue(queue.next()(), "One")

        queue.submit(lambda: "Three")
        self.assertTrue(queue.next()(), "Two")
        self.assertTrue(queue.next()(), "Three")

        queue.submit(lambda: "Four")
        queue.submit(lambda: "Five")
        self.assertTrue(queue.next()(), "Four")
        self.assertTrue(queue.next()(), "Five")

    def test_execute_out_of_order(self):
        queue = ExecutionQueue()
        queue.submit(lambda: "One")
        queue.submit(lambda: "Two", 0.2)
        queue.submit(lambda: "Three")
        queue.submit(lambda: "Four", 0.1)
        queue.submit(lambda: "Five")

        self.assertTrue(queue.next()(), "One")
        self.assertTrue(queue.next()(), "Three")
        self.assertTrue(queue.next()(), "Five")

        time.sleep(0.1)
        self.assertTrue(queue.next()(), "Four")

        time.sleep(0.1)
        self.assertTrue(queue.next()(), "Two")