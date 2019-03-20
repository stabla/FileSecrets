
import requests
import re

from bs4 import BeautifulSoup
from selenium import webdriver

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
    css = [i.get('href') for i in soup.find_all('link') if (i.get('href') and re.search('.css$', i.get('href')))]
    return css



parser = argparse.ArgumentParser()
parser.add_argument("url", help="target's url")
parser.add_argument("--depth", help="increase precision of the research through a webdriver", default=0)
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
    driver = webdriver.Chrome('driver/chromedriver')  # use Chrome driver for example
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(colored("URL/Domain: Must be specified", "blue"))
