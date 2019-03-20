import requests
import re
import tldextract
from bs4 import BeautifulSoup
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
import argparse
from termcolor import colored

## find js files
def getJSFiles(url):
    page = requests.get(url).text
    ##print(page)
    soup = BeautifulSoup(page, 'html.parser')
    print(colored("[*] Downloading js files...", "blue"))
    js = [i.get('src') for i in soup.find_all('script') if (i.get('src') and re.search('.js$', i.get('src')))]
    return js

## find css files
def getCSSFiles(url):
    page = requests.get(url).text
    ##print(page)
    soup = BeautifulSoup(page, 'html.parser')
    print(colored("[*] Downloading css files...", "blue"))
    css = [i.get('href') for i in soup.find_all('link') if (i.get('href') and re.search('.css$', i.get('href')) and sameDomain(i.get('href'), url))]
    return css

def sameDomain(fileUrl, initialUrl):
    domainName = tldextract.extract(initialUrl).domain

    ## is it starting with www/https/http?
    if (re.search("^(http|https)://", fileUrl) or re.search("^www.", fileUrl)):
        ## check the domain name and compare to initialUrl if it's from the same domain
        if (domainName not in fileUrl):
            ## not the same domain, it's probably a lib from cdn that we should ignore
            return False
    return True




parser = argparse.ArgumentParser()
parser.add_argument("url", help="target's url")
parser.add_argument("-d", "--depth", help="increase precision by checking dynamic files (require webdrive)", default=False)
parser.add_argument("-e", "--external", help="increase precision by analyzing external libraries", default=False)
args = parser.parse_args()

print(colored("=====================================================", "blue"))
print(colored(" FileSecrets                          v0.1  @stabla  ", "blue"))
print(colored("=====================================================", "blue"))

if args.url:
    url = args.url
    if "http" not in args.url:
        url = "http://" + args.url
        
    for jsFiles in getJSFiles(url):
        print(jsFiles)
    for cssFiles in getCSSFiles(url):
        print(cssFiles)

if args.depth:
    ## In depth, you need chrome driver and it will do a better inspect with dynamic js files
    print("depthturned on")
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('driver/chromedriver', options=options)  # use Chrome driver for example
    ## driver.set_window_position(-10000,0)
    print ("Running Headless Firefox Initialized")
    driver.get(url)
    driver.quit()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(colored("[*] Downloading css files...", "blue"))
