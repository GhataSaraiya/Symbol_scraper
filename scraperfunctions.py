from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from configparser import ConfigParser
import sys
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

timeout=5

#configure properties using 'app.config'
def configure():
    configur = ConfigParser() 
    configur.read('app.config')
    config={}
    config['url']=configur.get('scrapper','url')
    config['sector']=configur.get('scrapper','sector')
    config['datafile']=configur.get('scrapper','datafile')
    config['defaultsector']=configur.get('scrapper','defaultsector')
    config['driverpath']=configur.get('scrapper','driverpath')
    
    return(config)

#process commandline arguments
#structure:
#options: init, ip, op
#init-initialisation required
#ip- input filename present
#op- output filename present
#if some option is not present default values will be assigned
#defaults: init=False, ipfilename=symbols.txt, opfilename=result.json
def processArgs(args):
    n=len(args)
    if(n==0):
        return(False,'symbols.txt','result.json')
    options=args[0]
    init=False
    ipfilename='symbols.txt'
    opfilename='result.json'
    if('init' in options):
        init=True
    if('ip' in options and n>1):
        ipfilename=args[1]
        if('op' in options and n>2):
            opfilename=args[2]
        
        return(init,ipfilename,opfilename)
    
    if('op' in options and n>1):
        opfilename=args[1]

    return(init,ipfilename,opfilename)


#initalise selenium driver, load page and select sector
def initDriver(url,sector,defaultsector,driverpath):
    driver = webdriver.Chrome(driverpath)
    driver.get(url)
    dropdown=Select(driver.find_element_by_id('competitors-quote-sectors'))
    if(sector==defaultsector):
        return(driver)
    try:
        dropdown.select_by_visible_text(sector)
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'next'))
        WebDriverWait(driver, timeout).until(element_present)
        return(driver)
    except TimeoutException:
        print ("Timed out waiting for page to load")
        return(None)
    except NoSuchElementException:
        print("Invalid sector")
        return(None)
    

#take in a loaded page and traverse all available pages to generate data and store it in findata.json
def createJson(driver,datafile):
    symboldict={}
    while(1):
        soup=BeautifulSoup(driver.page_source,'html.parser')
        table=soup.find("table").find("tbody")
        rows=table.find_all("tr")
        for row in rows:
            cols=row.find_all("td")
            sym=cols[0].find("div").find("a").text
            name=cols[1].find("div").find("span").find("span").find("span").text
            symboldict[sym]=name
    
        try:
            driver.find_element_by_class_name('next').click()
            element_present = EC.presence_of_element_located((By.TAG_NAME, 'table'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            print ("Timed out waiting for page to load")
            return(None)
        except:
            break

    if(len(symboldict)!=503):
        return(None)

    jsondata=json.dumps([{'Symbol':key,'Name':value} for key,value in symboldict.items()])
    with open(datafile,'w') as findata:
        findata.write(jsondata)

    return(symboldict)


#check if initialisation is required otherwise read from findata
#returns symbol:name dictionary
def getSymData(init,url,sector,defaultsector,driverpath,datafile):
    
    if(init==True):
        driver=initDriver(url,sector,defaultsector,driverpath)
        if(driver==None):
            return(None)
        symdata=createJson(driver,datafile)
        driver.close()
    else:
        with open(datafile,'r') as finjson:
            findata=json.load(finjson)
            symdata={}
            for ele in findata:
                symdata[ele['Symbol']]=ele['Name']
    return(symdata)


#returns list of symbols present in file
def getSymbols(filename):
    symbols=[]
    with open(filename,'r') as symbol_file:
        symbols=symbol_file.readlines()
        symbols=[s.strip() for s in symbols]
    return symbols

    
#queries dict to create result json and store it in opfile
def querySymNameJson(query,data,opfilename):
    result={}
    for q in query:
        try:
            result[q]=data[q]
        except:
            result[q]='Name not found'
    resultjson=json.dumps([{'Symbol':key,'Name':value} for key,value in result.items()])
    with open(opfilename,'w') as opfile:
        opfile.write(resultjson)
    return(resultjson)


if __name__ =='__main__':
    nargs=len(sys.argv)
    args=[]
    if(nargs>1):
        args=sys.argv[1:]

    init,ipfilename,opfilename=processArgs(args)
    print("Parameters received: \n Initialisation required:",init,"\nInput file name: ",ipfilename,"\nOutput file name: ",opfilename,"\n")
    print("Default values assigned to empty fields")
    print("---------------------------------------")
    print("PROCESSING")
    config=configure()
    symdata=getSymData(init,config['url'],config['sector'],config['defaultsector'],config['driverpath'],config['datafile'])
    if(symdata==None):
        print("Error occured")
        exit()
    querySymbols=getSymbols(ipfilename)
    if(len(querySymbols)==0):
        print("Error occured")
        exit()
    results=querySymNameJson(querySymbols,symdata,opfilename)
    print("---------------------------------------")
    print("Query results:\n",results)
    print("Duplicated values have been removed.")
    exit()
    
    
    
    