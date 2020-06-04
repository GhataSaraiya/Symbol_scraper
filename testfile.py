import unittest
from scrapperfunctions import *

class TestInits(unittest.TestCase):

    def test_configure(self):
        self.assertEqual(configure(),('https://www.barchart.com/stocks/quotes/GOOG/competitors','Indices S&P 500'))

    def test_getSymbols(self):
        self.assertEqual(getSymbols('symbols.txt'),['GOOGL','MSFT'])
if __name__ =='__main__':
    unittest.main()