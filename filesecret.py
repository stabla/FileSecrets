import os, requests, re, tldextract, argparse, shutil
import mimetypes
import urllib
from bs4 import BeautifulSoup
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  

urllib.URLopener.version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser()
parser.add_argument("url", help="target's url")
parser.add_argument("-d", "--dynamic", help="increase precision by checking dynamic files (require webdriver)", type=str2bool, default=False)
parser.add_argument("-e", "--external", help="increase precision by analyzing external libraries (third-parties components)", type=str2bool, default=False)
parser.add_argument("-k", "--keep", help="keep file when downloaded, do not remove them", type=str2bool, default=False)
parser.add_argument("-w", "--word", help="add some words to the original library", default="")
parser.add_argument("-dic", "--dictionnary", help="use your own dictionnary of words", type=str2bool, default=True)
args = parser.parse_args()

pathFiles = []
downloadedFiles = []
folder = 'binder/'

## find js files
def getJSFiles(url):
    print(colored("[*] Retrieving js files...", "blue"))
    js = [i.get('src') for i in soup.find_all('script') if (i.get('src') and re.search('.js$', i.get('src')) and (args.external or sameDomain(i.get('src'), url)))]
    for i in js: pathFiles.append(i)
    return js

## find css files
def getCSSFiles(url):
    print(colored("[*] Retrieving css files...", "blue"))
    css = [i.get('href') for i in soup.find_all('link') if (i.get('href') and re.search('.css$', i.get('href')) and (args.external or sameDomain(i.get('href'), url)))]
    for j in css: pathFiles.append(j)
    return css

## find html, php files files
def getHTMLFiles(url):
    print(colored("[*] Retrieving html files...", "blue"))
    html = [i.get('href') for i in soup.find_all('a') if (i.get('href') and re.search('.php|.html$', i.get('href')) and (sameDomain(i.get('href'), url)))]
    for i in soup.find_all('a'):
        if (i.get('href') and re.search('.*$', i.get('href')) and (sameDomain(i.get('href'), url) == False)):
            print(colored("     [!] There's a pointer to an external website: " + i.get('href') + " - Not going further", "grey", attrs=['bold']))
    for k in html: pathFiles.append(k)
    return html

## find all others, with no extension
def getOtherFiles(url):
    print(colored("[*] Retrieving other files...", "blue"))
    other = [i.get('href') for i in soup.find_all('a') if (i.get('href') and re.search('^(?!mailto:|ftp://|^#$|.*\.css$|.*\.html|.*\.php)', i.get('href')) and (sameDomain(i.get('href'), url)))]
    ## for unknown extension
    for i in other:
        last_url_part = i.rsplit('/', 1)
        print("     [+] " + last_url_part[1] + " (unknown extension)")
        urllib.urlretrieve(i, folder + last_url_part[1] + ".txt")
        downloadedFiles.append(last_url_part[1] + ".txt")
    for l in other: pathFiles.append(l)

    
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
        print("ici ")
        print(url)
        downloadedFiles.append(file_name)
        # Download the file from `url` and save it locally under `file_name`:
        urllib.urlretrieve(url, folder + file_name)

## download the homepage
def downloadOrigin(intiialUrl):
    url = intiialUrl
    downloadedFiles.append("HOME_PAGE.html")
    urllib.urlretrieve(url, folder + "HOME_PAGE.html")

def downloadFile(url):
    urllib.URLopener.version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0'
    print(url)
    urllib.urlretrieve(url, folder + "INITIAL.html")
    #urllib.urlretrieve(url, folder + "INTIIAL.html")

## open the and search in it
def digger(fileName):
    words = []
    if (args.dictionnary == True):
        with open("secrets.txt", "r") as f: words = [line.rstrip('\n \t') for line in f]
    if (args.word != ""):
        just_word = [x.strip() for x in args.word.split(',')]
        words.extend(just_word)
    else:
        regex = "\\b" + "\\b|\\b".join(words) + "\\b"
        for i, line in enumerate(open(folder + fileName)):
            for match in re.finditer(regex, line, flags=re.IGNORECASE):
                print(colored("         [*] Found word : '" + match.group(0) + "' at line " + str(i+1) + " in " + fileName, "red"))

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

def main():
    if args.url:

        ## downloadOrigin(url)
        print(url)
        downloadFile(url)
        print("la apres downloadOrigin")

        ## check the dynamic given as argument (optional)
        ## In dynamic, you need chrome driver and it will do a better inspect with dynamic js file
        if args.dynamic:
            print(colored("=====================================================", "blue"))
            print (colored("Running Headless Chrome Initialized", "blue"))
            options = Options()
            options.headless = True
            driver = webdriver.Chrome('driver/chromedriver', options=options)  # use Chrome driver for example
            driver.set_window_position(-10000,0)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
      
        '''
        for jsFiles in getJSFiles(url):
            print("     [+] " + jsFiles)
            downloadLocally(jsFiles, url)
            print('apres js downloadLocally')
        print(colored("[OK] Downloaded js files. ", "blue"))

        ### print(pathFiles)

        ## CHECK FOR CSS FILES
        for cssFiles in getCSSFiles(url):
            print("     [+] " + cssFiles)
            downloadLocally(cssFiles, url)
        print(colored("[OK] Downloaded css files. ", "blue"))

        ## CHECK FOR HTML FILES
        for htmlFiles in getHTMLFiles(url):
            print("     [+] " + htmlFiles)
            downloadLocally(htmlFiles, url)
        print(colored("[OK] Downloaded html files. ", "blue"))
        print(colored("[OK] Downloaded all other files... ", "blue"))
        getOtherFiles(url)
        print(colored("[*] List of files currently downloaded locally", "blue"))
        print("     "  + u", ".join(downloadedFiles))
        print(colored("[*] Starting the digging in files... ", "blue"))
        if ((args.dictionnary == False) and (args.word == "")):
            print(colored("/!\ ERROR: NO DICTIONNARY AND NO WORDS.", "magenta"))
        else:
            ## digging in found file
            for i in downloadedFiles:
                print(colored("     [-] Checking in " + i, "blue"))
                digger(i)
            
            ## delete all files in the folder binder/
            if (args.keep == False):
                print(colored("[*] Deleting all files downloaded previously", "blue"))
                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(e)
        '''
    else:
        print(colored("/!\ ERROR: NO URL.", "magenta"))

    












## CHECKS ARGUMENTS
if ((args.dictionnary == False) and (args.word == "")):
    print(colored("/!\ ERROR: NO DICTIONNARY AND NO WORDS.", "magenta"))
else:
    url = args.url
    print(colored("=====================================================", "blue"))
    print(colored(" url : " + args.url, "blue"))
    a = 'true' if args.dynamic else 'false'
    print(colored(" dynamic : " + a, "blue"))

    b = 'true' if args.external else 'false'
    print(colored(" external : " + b, "blue"))

    c = 'true' if args.keep else 'false'
    print(colored(" keep files : " + c, "blue"))

    d = 'false' if (args.word == '') else 'true'
    print(colored(" custom words : " + d, "blue"))

    e = 'true' if (args.dictionnary == True) else 'false'
    print(colored(" use dictionnary : " + e, "blue"))
    print(colored("=====================================================", "blue"))

    ## format url
    url = formatUrlInput(args.url)

    if "http" not in url:
        url = "http://" + url
    cpt = 0

    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    

    main()