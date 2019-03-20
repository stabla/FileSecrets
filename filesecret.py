
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from termcolor import colored

url = 'http://guillaumebonnet.fr'
ext = 'js'

## In depth, you need chrome driver
driver = webdriver.Chrome('driver/chromedriver')  # use Chrome driver for example

def listFD(url, ext=''):
    ##page = requests.get(url).text
    ##print(page)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    js = [i.get('src') for i in soup.find_all('script') if i.get('src')]
    return js



driver.get(url)
for file in listFD(url, ext):
    print(file)



## TERMCOLOR ADDED
## print(colored('hello', 'red'), colored('world', 'green'))