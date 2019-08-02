# coding: utf-8
try:  
    import json  
except ImportError:  
    import simplejson as json
import http.cookiejar as cookielib
import requests
from bs4 import BeautifulSoup
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
dbname="cookidoo"
colname="cookidoo.com.cn"
idstrart=0
idend=1000000

def docproc (itemid):
    soup = BeautifulSoup(r.text, 'html.parser')
    
    mydict = { "ID": itemid, "rawscript0":str(soup.find(type="application/ld+json")) ,"rawscript1": str(soup.find(type="text/javascript")),"rawimage0": str(soup.find(property="og:image")),"rawrelationship": str(soup.find(id="in-collections"))}
    result = mycol.insert_one(mydict) 
    print(result)
    return

cookie_jar = cookielib.MozillaCookieJar()
cookies = open('C:\\Users\\franc\\OneDrive\\Desktop\\cookidoo.txt').read()
for cookie in json.loads(cookies):
  cookie_jar.set_cookie(cookielib.Cookie(version=0, name=cookie['name'], value=cookie['value'], port=None, port_specified=False, domain=cookie['domain'], domain_specified=False, domain_initial_dot=False, path=cookie['path'], path_specified=True, secure=cookie['secure'], expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False))
dblist = myclient.list_database_names()
if dbname in dblist:
    print("database " +colname+" already existed in dblist")
mydb = myclient[dbname]
collist = mydb. list_collection_names()
if colname in collist:
    print("collection "+colname+" already existed in mydb")
mycol = mydb[colname]

tempurl=''
urlvar=idstrart-1
while urlvar<=idend:
    urlvar+=1
    tempurl='https://cookidoo.com.cn/recipes/recipe/zh-Hans/r'+str(urlvar)
    print(tempurl)
    try: 
        r = requests.get(tempurl,cookies=cookie_jar)
    except Exception:
        print("Request current HTML document error, try again")
        urlvar=urlvar-1
    else:
        if(r.status_code == 200):
            print(str(urlvar)+' OK')
            docproc(urlvar)
        else:
            print(str(urlvar)+' EMPTY')


