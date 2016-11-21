# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 22:05:14 2016

@author: Shriharsh Ambhore
@author: Kandhasamy Rajasekaran
@author: Daniel Akbari
"""

#from assignment4_bravo_Q1_http import downloadResource
import urllib

import os
import socket
import re
import time

import sys
import urllib
from assignment4_bravo_functions import *


def extractImageUrl(fileLocation):
    urllist=[]
    pattern=re.compile('src="([^"]+)"') # regex for extracting the value of src attribute
    hrefPattern=re.compile('href="([^"]+)"')
    with  open(fileLocation) as f:
        for l in f:
            #print("**** currently reading::",l)
            if "<img" in l:
                matches = re.findall(pattern,l)
                urllist.append(matches[0])
                #print("****** found an img tab:")
            elif "<link" in l:
                found=re.findall(hrefPattern,l)
                urllist.append(found[0])
                

    return urllist

#fileLoc=input("Enter the html file location of the downloaded file:")
fileLoc = 'index.html'
#fileLoc="C:\\Users\\ShreeH\\resource"
#inputurl=input("Enter the url from which the file was downloaded:")
inputurl='http://west.uni-koblenz.de'

urlObj = urllib.parse.urlparse(inputurl)
urlScheme = urlObj[0] #http
urlDomain = urlObj[1] #full domain name
urlPath = urlObj[2]


listOfURL=extractImageUrl(fileLoc)
print("List of URLs",listOfURL)
  


# iterate over the url to download the image 
for url in listOfURL:
   
    try:
        socClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socClient.connect((urlDomain, 80))
        path=urllib.parse.urlparse(url).path
        imageName=(path[path.rfind("/")+1:])
        tempUrl = url
        if url.find(inputurl)== -1:
            #append the input url to construct the absolute path for the image
            tempUrl=inputurl+url
      
        downloadResource(socClient,tempUrl)        
        socClient.close()
    except socket.error as e:
       print('Connection Invalid. Input proper URL !!!',e)
    except:
        print('Connection Invalid. Input proper URL !!!')

url=None
data=None 

            
    


