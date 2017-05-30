#!/usr/bin/python

import json
import urllib2
from bs4 import BeautifulSoup
import requests
import os.path



print("Enter the name of the song: ")
song=str(raw_input())

print("Save to which directory? ")
directory=str(raw_input())


if not os.path.exists(str(directory)):
	os.mkdir(str(directory))

directory_path = str(os.path.abspath(str(directory)))

url="https://www.youtube.com/results?search_query=" + str(song)
pagesource=requests.get(str(url))
s=pagesource.text
soup=BeautifulSoup(s)
for link in soup.find_all('a'):
    temp=link.get('href')
    if("/watch?v=" in str(temp)):
    	final_url=temp
    	break
api="http://www.youtubeinmp3.com/fetch/?format=JSON&video=http://www.youtube.com"+str(final_url)
response=urllib2.urlopen(str(api))
data=json.loads(response.read())
download_link=data['link']
#print(str(download_link))

url = str(download_link)

#print(str(url))

file_name = str(song)
u = urllib2.urlopen(str(url))
file_name=os.path.join(str(directory_path),str(file_name))+".mp3"
f = open(file_name, 'wb')
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print "Downloading: %s Bytes: %s" % (file_name, file_size)

file_size_dl = 0
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break

    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print status,

f.close()
