import requests
import hashlib
from bs4 import BeautifulSoup
import sys
import time

siteHashMaping = {}
siteTimeMaping = {}

def makeHttpRequest(url):
    url = addhttp(url)
    r= None
    try:
        r = requests.get(url)
        r.encoding = 'UTF-8'
        if(r.status_code == 200):
            #print("Requset send to " + r.url)
            r.encoding = 'ISO-8859-1'
    except requests.exceptions.ConnectionError:
        #site not found
        r = None
    
    return r

def getSiteHash(url,mode = "hardcoded"):
    request = makeHttpRequest(url)
    if(request is None):
        raise requests.exceptions.ConnectionError
    
    text = (request.text).encode("utf-8")
    
    return getHash(text,mode)
    

def getHash(siteTextCode,mode = "hardcoded"):
    m = hashlib.sha256()
    if(mode == "hardcoded"):
        m.update(siteTextCode)
    elif(mode == "gk"):
        soup = BeautifulSoup(siteTextCode, 'html.parser')
        text = str(soup.find_all('p')).encode("utf-8")
        text = text  + str(soup.find_all('a')).encode("utf-8")
        text = text  + str(soup.find_all('h1')).encode("utf-8")
        text = text  + str(soup.find_all('h2')).encode("utf-8")
        text = text  + str(soup.find_all('h3')).encode("utf-8")
        text = text  + str(soup.find_all('img')).encode("utf-8")
        text = text  + str(soup.find('title')).encode("utf-8")
        m.update(text)
    
    textHash = m.hexdigest()
    return textHash
    
def isSiteChanged(url,txtHash):
    if(getSavedHash(url) == 'Empty'):
        #print("Site Added: " + url)
        return True , "New"
    elif(not getSavedHash(url) == txtHash):
        #print("Has changed: " + url)
        return True
    else:
        #print("Not changed")
        return False

def getSavedHash(url):
    return siteHashMaping.get(url, 'Empty')

def updateSavedHash(url,txtHash):
    siteHashMaping[url] = txtHash


def updateSavedTime(url):
    #2012-04-23T18:25:43.511Z
    siteTimeMaping[url] = time.strftime("%Y-%m-%dT%H:%M:%SZ")

def getLastChange(url):
    return siteTimeMaping.get(url, 'Never')
def addhttp(url):
    return "http://" + url
def stripHttp(url):
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    return url