import unittest


class TestCaseA(unittest.TestCase):

    def test_foo(self):
        pass

    def test_bar(self):
        self.fail()
