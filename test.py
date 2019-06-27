import urllib.request
req = urllib.request.Request(
    url = "http://guillaumebonnet.fr/js/app.js", 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

folder = 'binder/'
f = urllib.request.urlopen(req)
e = open( folder + 'INITI.html', 'w' )
e.write( f.read().decode('utf-8') )
e.close()

