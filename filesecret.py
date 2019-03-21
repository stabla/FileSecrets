import os, requests, re, tldextract, argparse, shutil
import urllib.request
from bs4 import BeautifulSoup
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  

parser = argparse.ArgumentParser()
parser.add_argument("url", help="target's url")
parser.add_argument("-d", "--dynamic", help="increase precision by checking dynamic files (require webdriver)", default=False)
parser.add_argument("-e", "--external", help="increase precision by analyzing external libraries", default=False)
parser.add_argument("-k", "--keep", help="keep file when downloaded, do not remove them", default=False)
args = parser.parse_args()

downloadedFiles = []

## find js files
def getJSFiles(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    print(colored("[*] Retrieving js files...", "blue"))
    js = [i.get('src') for i in soup.find_all('script') if (i.get('src') and re.search('.js$', i.get('src')) and (args.external or sameDomain(i.get('src'), url)))]
    ## for j in js:
        ## print(j)
    return js

## find css files
def getCSSFiles(url):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    print(colored("[*] Retrieving css files...", "blue"))
    css = [i.get('href') for i in soup.find_all('link') if (i.get('href') and re.search('.css$', i.get('href')) and (args.external or sameDomain(i.get('href'), url)))]
    return css

## verify if the file is hosted on the given URL
def sameDomain(fileUrl, initialUrl):
    domainName = tldextract.extract(initialUrl).domain
    ## is it starting with www/https/http?
    if (re.search("^(http|https)://", fileUrl) or re.search("^www.", fileUrl)):
        ## check the domain name and compare to initialUrl if it's from the same domain
        if (domainName not in fileUrl):
            ## not the same domain, it's probably a lib from cdn that we should ignore
            return False
    return True

## get the filename with its extension
def getFileURI(URL):
    filename_w_ext = os.path.basename(URL)
    filename, file_extension = os.path.splitext(filename_w_ext)
    return filename + '' + file_extension

## download a file
def downloadLocally(fileUrl, initialUrl):
    if sameDomain(fileUrl, initialUrl):
        ## download on intiialUrl + fileUrl
        url = initialUrl + fileUrl
        file_name = getFileURI(fileUrl)
        downloadedFiles.append(file_name)
        # Download the file from `url` and save it locally under `file_name`:
        urllib.request.urlretrieve(url, "binder/" + file_name)

## open the and search in it
def digger(fileName):
    with open("secrets.txt", "r") as f: words = [line.rstrip('\n \t') for line in f]
    regex = "\\b" + "\\b|\\b".join(words) + "\\b"
    for i, line in enumerate(open('binder/' + fileName)):
        for match in re.finditer(regex, line, flags=re.IGNORECASE):
            print(colored(" [*] Found word : '" + match.group(0) + "' at line " + str(i+1) + " in " + fileName, "red"))

## used as middleware, should be used first to correctly format url
def formatUrlInput(url):
    url = url
    if (not re.search("^www.", url) and (not re.search("^(http|https)://", url))):
        url = "www." + url
    if (not url.endswith('/')):
        url = url + '/'
    return url

###############
## user menu ##
###############
print(colored("=====================================================", "blue"))
print(colored(" FileSecrets                          v0.1  @stabla  ", "blue"))

if args.url:
    url = args.url
    print(colored("=====================================================", "blue"))
    print(colored(" url : " + args.url, "blue"))
    a = 'true' if args.dynamic else 'false'
    print(colored(" dynamic (not done yet) : " + a, "blue"))

    b = 'true' if args.external else 'false'
    print(colored(" external : " + b, "blue"))
    print(colored("=====================================================", "blue"))

    ## format url
    url = formatUrlInput(args.url)

    if "http" not in url:
        url = "http://" + url
    cpt = 0

    print(colored(url, "red"))

    for jsFiles in getJSFiles(url):
        print(jsFiles)
        downloadLocally(jsFiles, url)
    print(colored("[OK] Downloaded js files. ", "blue"))

    for cssFiles in getCSSFiles(url):
        print(cssFiles)
        downloadLocally(cssFiles, url)
    print(colored("[OK] Downloaded css files. ", "blue"))

    print(colored("[*] List of files currently downloaded locally", "blue"))
    print(downloadedFiles)
    
    print(colored("[*] Starting the digging in files... ", "blue"))
    digger("basesign.css")
else:
    print(colored("/!\ ERROR: NO URL.", "purple"))

## check the dynamic given as argument (optional)
## In dynamic, you need chrome driver and it will do a better inspect with dynamic js file
if args.dynamic:
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('driver/chromedriver', options=options)  # use Chrome driver for example
    driver.set_window_position(-10000,0)
    print ("Running Headless Chrome Initialized")
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(colored("[*] Downloading css files...", "blue"))

## delete all files in the folder binder/
if (args.keep == False):
    folder = 'binder/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

