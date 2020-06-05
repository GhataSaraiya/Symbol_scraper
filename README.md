# Symbol_scrapper


Web scraping application which scrapes data from <https://www.barchart.com/stocks/quotes/GOOG/competitors> to get information about company symbols and names using Selenium and BeautifulSoup.
The scraped information is stored in form of json objects which is then used to query names using symbols.


Files:
 - scraperfunctions.py: Code file containing the scraping and querying logic
 - testfile.py: Unit testing code
 - app.config: configuration file
 - findata.json: stores all financial data(scraped)
 - symbols.txt: default symbol file for querying
 - result.json: default output file for storing queried data
 - testdata.json and test.json: used for unit testing
 - chromedriver.exe: web driver for chrome (required for selenium)
 - runscraper.sh: shell script file to run scraper


Options available with the scraperfunctions.py, which can be provided using command line arguments:
 - init: Initialisation required, if mentioned scraping process will be performed from scratch.
 - ip: Input file name present, if mentioned the specified filename will be used for obtaining query symbols.
 - op: Output file name present, if mentioned the specified filename will be used for obtaining queried data.


Configuration details:
 - url: Specifies the url to be used for scraping
 - sector: Specifies the sector which needs to be selected for querying, we use Indices S&P 500
 - datafile: The file that needs to be used to store scraped data
 - defaultsector: The sector which is initially loaded when the request is made.
 - driverpath: The path for selenium driver


