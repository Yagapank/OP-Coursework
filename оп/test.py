import unittest
from Levenstein import *

class Test(unittest.TestCase):
    def test_Levenstein(self):
        test = Levenstein()
        self.assertEqual(test.levenstein('TUSUR', 'TUSER'), 1)

    def test_Levenstein2(self):
        test = Levenstein()
        self.assertEqual(test.levenstein('WORLD', 'WORLL'), 1)

    def test_Levenstein3(self):
        test = Levenstein()
        self.assertNotEqual(test.levenstein('TUSUR', 'TUSER'), 2)


