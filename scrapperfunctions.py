from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from configparser import ConfigParser
import sys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
    timeout=5
    try:
        dropdown.select_by_visible_text(sector)
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'next'))
        WebDriverWait(driver, timeout).until(element_present)
        return(driver)
    except TimeoutException:
        print ("Timed out waiting for page to load")
        return(None)
    

def getSymbols(filename):
    symbols=[]
    with open(filename,'r') as symbol_file:
        symbols=symbol_file.readlines()
        symbols=[s.strip() for s in symbols]
    return symbols

def createJson(driver):
    symboldict={}
    pgNo=1
    timeout=5
    while(pgNo<=6):     
        soup=BeautifulSoup(driver.page_source,'html.parser')
        table=soup.find("table").find("tbody")
        rows=table.find_all("tr")
        for row in rows:
            cols=row.find_all("td")
            sym=cols[0].find("div").find("a").text
            name=cols[1].find("div").find("span").find("span").find("span").text
            symboldict[sym]=name
        if(pgNo==6):
            break
    
        try:
            driver.find_element_by_class_name('next').click()
            element_present = EC.presence_of_element_located((By.TAG_NAME, 'table'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print ("Timed out waiting for page to load")
            return(None)
        pgNo+=1 
    if(len(symboldict)!=503):
        return(None)

    jsondata=json.dumps([{'Symbol':key,'Name':value} for key,value in symboldict.items()])
    with open('findata.json','w') as findata:
        findata.write(jsondata)

    return(symboldict)
    

def getSymNameJson(query,data,opfilename):
    result={}
    for q in query:
        try:
            result[q]=data[q]
        except:
            result[q]='Name not found'
    resultjson=json.dumps([{'Symbol':key,'Name':value} for key,value in result.items()])
    with(opfilename,'w') as opfile:
        opfile.write(resultjson)
    return(resultjson)

if __name__ =='__main__':
    nargs=len(sys.argv)
    if(nargs>2):
        options=sys.argv[2]

        if('init' in options):
            url,sector=configure()
            driver=initDriver(url,sector)
            symdata=createJson(driver)
            driver.close()
        else:
            with open('findata.json','r') as finjson:
                findata=json.load(finjson)
                symdata={}
                for ele in findata:
                    symdata[ele['Symbol']]=ele['Name']
        
        if('ip' in options and nargs>3):
            ipfilename=sys.argv[3]
            if('op' in options and nargs==5):
                opfilename=sys.argv[4]
            else:
                opfilename='result.json'
        elif('op' in options and nargs>3):
            opfilename=sys.argv[3]
        else:
            opfilename='result.json'

    querySymbols=getSymbols(ipfilename)
    results=getSymNameJson(querySymbols,symdata,opfilename)
    print(results)
    
    
    