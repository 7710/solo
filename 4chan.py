#!/usr/bin/python
import requests
import os
import time
import urllib
from lxml import etree
from requests.packages import urllib3
""" 批量下载4chan页面中的图片
"""


def timeft(t, fs="%Y-%m-%d %H:%M:%S"):
    return time.strftime(fs, t)


def geturls():
    """ 获取配置文件内的url列表
        配置文件与脚本同名，无后缀
    """
    a = []
    s = os.path.basename(__file__).split('.')[0]
    if not os.path.exists(s):
        return a
    with open(s) as f:
        l = f.readline()
        while l:
            a.append(l.strip())
            l = f.readline()
    return a


def writeimg(img, path):
    """ 保存图片
    """
    conn = urllib.request.urlopen("http:" + img, timeout=30)
    f = open(path, 'wb')
    f.write(conn.read())
    f.close()


def getimg(link, path):
    """ 获取图片url
    """
    img = link.attrib.get("href")
    filename = img.split('/')[-1]
    filepath = "%s/%s" % (path, filename)
    if os.path.isfile(filepath):
        return
    print(filename)
    n = 0
    while n < 3:
        try:
            writeimg(img, filepath)
            time.sleep(3)
        except:
            n += 1
            print("retry %d" % n)
        else:
            break


def main():
    # 保存路径
    _PATH = "/home/public/Pictures/4chan"
    urls = geturls()
    for url in urls:
        print(url)
        ua = url.split('/')
        path = "%s/%s" % (_PATH, ua[-3])
        if not os.path.exists(path):
            os.makedirs(path)
        path = "%s/%s" % (path, ua[-1])
        if not os.path.exists(path):
            os.makedirs(path)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        r = requests.get(
            url=url, allow_redirects=False, verify=False, timeout=30)
        content = r.content.decode('ISO-8859-1')
        html = etree.HTML(content)
        links = html.xpath("//a[@class='fileThumb']")
        for link in links:
            getimg(link, path)


if __name__ == '__main__':
    main()
