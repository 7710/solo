#!/usr/bin/python
import requests
import os
import sys
import time
import urllib
from lxml import etree

def timeft(t, fs="%Y-%m-%d %H:%M:%S"):
    return time.strftime(fs, t)

def main():
    _PATH = "/home/sunq/Pictures/4chan"
    urls = ["http://boards.4chan.org/s/thread/18447811"
                #, "http://boards.4chan.org/s/thread/18439093"
                #, "http://boards.4chan.org/s/thread/18441231"
            ]
    for url in urls:
        ua = url.split('/')
        path = "%s/%s" % (_PATH, ua[-3])
        if not os.path.exists(path):
            os.makedirs(path)
        path = "%s/%s" % (path, ua[-1])
        if not os.path.exists(path):
            os.makedirs(path)
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        r = requests.get(url=url,
                         allow_redirects=False,
                         verify=False,
                         timeout=30)
        content = r.content.decode('ISO-8859-1')
        #html = etree.HTML(content.decode('utf-8'))
        html = etree.HTML(content)
        links = html.xpath("//a[@class='fileThumb']")
        for link in links:
            img = link.attrib.get("href")
            filename = img.split('/')[-1]
            print("%s-%s" % (ua[-3], filename))
            filepath = "%s/%s" % (path, filename)
            if not os.path.isfile(filepath):
                conn = urllib.request.urlopen("http:"+img, timeout=30)
                f = open(filepath, 'wb')
                f.write(conn.read())
                f.close()
                time.sleep(3)

if __name__ == '__main__':
    main()

