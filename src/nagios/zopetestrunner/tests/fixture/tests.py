import unittest


class TestCase(unittest.TestCase):

    def test_foo(self):
        pass

    def test_bar(self):
        self.fail()

    def test_baz(self):
        raise RuntimeError
