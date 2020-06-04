import unittest
from scrapperfunctions import *
import json

class TestInits(unittest.TestCase):

    def test_configure(self):
        self.assertEqual(configure(),('https://www.barchart.com/stocks/quotes/GOOG/competitors','Indices S&P 500'))

    def test_getSymbols(self):
        self.assertEqual(getSymbols('symbols.txt'),['GOOGL','MSFT'])

    def test_createJson(self):
        url,sector=configure()
        driver=initDriver(url,sector)
        result=createJson(driver)
        self.assertNotEqual(result,None)
        with open('testdata.json','r') as testjson:
            testdata=json.load(testjson)
            testdict={}
            for ele in testdata:
                testdict[ele['Symbol']]=ele['Name']
        self.assertEqual(result,testdict)
        driver.close()
if __name__ =='__main__':
    unittest.main()