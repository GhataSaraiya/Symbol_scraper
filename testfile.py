import unittest
from scraperfunctions import *
import json

class TestInits(unittest.TestCase):

    def test_configure(self):
        c={'url': 'https://www.barchart.com/stocks/quotes/GOOG/competitors', 'sector': 'Indices S&P 500', 'datafile': 'findata.json', 'defaultsector': 'Internet - Services', 'driverpath': './chromedriver.exe'}
        self.assertEqual(configure(),c)

    def test_getSymbols(self):
        self.assertEqual(getSymbols('sym1.txt'),['GOOGL','MSFT','AAPL','CL'])

    def test_processArgs(self):
        self.assertEqual(processArgs([]),(False,'symbols.txt','result.json'))
        self.assertEqual(processArgs(['ip','sym.txt']),(False,'sym.txt','result.json'))
        self.assertEqual(processArgs(['op','res.json']),(False,'symbols.txt','res.json'))
        self.assertEqual(processArgs(['ipop','sym.txt','res.json']),(False,'sym.txt','res.json'))
        self.assertEqual(processArgs(['opip','sym.txt','res.json']),(False,'sym.txt','res.json'))
        self.assertEqual(processArgs(['initop','res.json']),(True,'symbols.txt','res.json'))
        self.assertEqual(processArgs(['initipop','sym.txt','res.json']),(True,'sym.txt','res.json'))

    def test_createJson(self):
        c={'url': 'https://www.barchart.com/stocks/quotes/GOOG/competitors', 'sector': 'Indices S&P 500', 'datafile': 'findata.json', 'defaultsector': 'Internet - Services', 'driverpath': './chromedriver.exe'}

        url,sector,defaultsector,driverpath=c['url'],c['sector'],c['defaultsector'],c['driverpath']
        driver=initDriver(url,sector,defaultsector,driverpath)
        result=createJson(driver,c['datafile'])
        driver.close()
        self.assertNotEqual(result,None)
        with open('testdata.json','r') as testjson:
            testdata=json.load(testjson)
            testdict={}
            for ele in testdata:
                testdict[ele['Symbol']]=ele['Name']
        self.assertEqual(result,testdict)
        driver.close()


#getSymData integrates calls when true: not to be tested when unit testing
    def test_getSymData(self):
        with open('testdata.json','r') as testjson:
            testdata=json.load(testjson)
            testdict={}
            for ele in testdata:
                testdict[ele['Symbol']]=ele['Name']
        self.assertEqual(getSymData(False,'https://www.barchart.com/stocks/quotes/GOOG/competitors','Indices S&P 100','Internet - Services','./chromedriver.exe','findata.json'),testdict)

    def test_querySymNameJson(self):
        query=['AAPL','A']
        data={'AAPL':'Apple Inc','MSFT':'Microsoft Corp'}
        opfile='test.json'
        self.assertEqual(querySymNameJson(query,data,opfile),'[{"Symbol": "AAPL", "Name": "Apple Inc"}, {"Symbol": "A", "Name": "Name not found"}]')

if __name__ =='__main__':
    unittest.main()