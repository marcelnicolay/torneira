try:
    import unittest2 as unittest
except ImportError:
    import unittest

from torneira.testing.client import TestingClient

class TestCase(unittest.TestCase):
    
    def __init__(self, *args, **kargs):
        self.client = TestingClient()
        super(TestCase, self).__init__(*args, **kargs)