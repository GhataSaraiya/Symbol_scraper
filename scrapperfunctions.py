from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from configparser import ConfigParser
import sys

def configure():
    configur = ConfigParser() 
    configur.read('app.config')
    url=configur.get('scrapper','url')
    sector=configur.get('scrapper','sector')
    return(url,sector)


def initDriver(url,sector):
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get(url)
    dropdown=Select(driver.find_element_by_id('competitors-quote-sectors'))
    dropdown.select_by_visible_text(sector)
    return(driver)

def getSymbols(filename):
    symbols=[]
    with open(filename,'r') as symbol_file:
        symbols=symbol_file.readlines()
        symbols=[s.strip() for s in symbols]
    return symbols


if __name__ =='__main__':
    url,sector=configure()
    driver=initDriver(url,sector)
    if(len(sys.argv)>1):
        filename=sys.argv[1]
    else:
        filename='symbols.txt'
    print(getSymbols(filename))
    driver.close()
    