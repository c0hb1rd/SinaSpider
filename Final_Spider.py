#!/usr/bin/env python
# coding:utf-8
import requests as re
import re as R
import time
import os
import Image
import cv2
from threading import Thread
from bs4 import BeautifulSoup
import sys
import json


## URL For User Image Json Page
# http://m.weibo.cn/page/json?containerid=103003index-*-UserID-*-_-_photo_all_l&page=1&retcode=6102, e.g: 1075567392
## End

## URL For User Home Json Page
# http://m.weibo.cn/u/-*-UserID-*-, e.g: 1075567392
## End

## Url For User information Page
# http://m.weibo.cn/page/card?itemid=100505-*-UserID-*-_-_WEIBO_INDEX_PROFILE_APPS&callback=_1467532491343_4&retcode=6102, e.g: 1075567392
## End

# Set Default Encode
reload(sys)
sys.setdefaultencoding('utf-8')

# Default Cookie
HEADERS = {
    'Cookie':''
}

# Cookie For URL: http://m.weibo.cn/users/-*-UserID-*-
HEADERS_FOR_GET_INFO = {
    'Cookie':''
}


# Get User Image Links, Return List
def getImageLinks(uid, page, headers=HEADERS):
    while True:
        try:
            imgLinks = []

            content = ''
            url = "http://m.weibo.cn/page/json?containerid=103003index%d_-_photo_all_l&page=%d&retcode=6102" % (uid, page)
            reponse = re.get(url, headers=headers)
            reponse.close()

            if reponse:
                content = reponse.content.replace('\\', '')
            data = json.loads(content)

            for src in data['cards'][0]['card_group'][0]['pics']:
                imgLinks.append(src['pic_ori'])

            return imgLinks
        except:
            continue


# Download Image
def downloadImage(imgUrl, path, filename, count):
    while True:
        try:
            r = requests.get(imgUrl, stream=True)
            with open(path + filename, 'wb') as f:
                for buff in r.iter_content(chunk_size=1024):
                    if buff:
                        f.write(buff)
                        f.flush()
            break
        except:
            continue
    print '[*]Download complete(%d)' % count


# Get User Fans Total, Return Int
def getUserFans(uid, headers=HEADERS):
    url = "http://m.weibo.cn/page/card?itemid=100505%d_-_WEIBO_INDEX_PROFILE_APPS&callback=_1467532491343_4&retcode=6102" % uid
    reponse = re.get(url, headers=headers)
    reponse.close()

    content = reponse.content.replace('\\', '')
    data = json.loads(content[17:-1])
    fans = data['apps'][3]['count'].split('u')

    if len(fans) > 1:
        if fans[1] == '4ebf':
            totalFans = fans[0] + '00000000'
            return int(totalFans)
        elif fans[1] == '4e07':
            totalFans = fans[0] + '0000'
            return int(totalFans)
    else:
        return int(fans[0])


# Detect Image whether Has Faces
def detectFaces(imageName):
    img = cv2.imread(imageName)
    faceCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    faces = faceCascade.detectMultiScale(gray, 1.2, 5)
    if faces == []:
        return False
    else:
        result = []
        for (x, y, width, height) in faces:
            result.append((x, y, x+width, y+height))
        return result


# Judge The User Fans Greater Than 'fans'
def isGreaterThan(info, fans):
    if info['粉丝'] > fans:
        return True
    else:
        return False


# Get User Information, Return Dict
def getUserInformation(uid, headers=HEADERS_FOR_GET_INFO):
    url = "http://m.weibo.cn/users/%d?retcode=6102" % uid
    reponse = re.get(url, headers=HEADERS_FOR_GET_INFO)
    reponse.close()

    content = BeautifulSoup(reponse.content.replace("\\", '').replace("rn", ""), "lxml")
    content = content.find_all('div', 'item-info-page')

    ls = {}
    for v in content:
        key = str(v.find('span'))[6:-7]
        value = str(v.find('p'))[3:-4]
        if key == '备注':
            continue
        elif key[-12:] == '微博认证':
            key = key[-12:]
        ls[key] = value
    ls['粉丝'] = getUserFans(uid)
    ls['UID'] = uid
    return ls

# 1075567392
# 1774543811

def main(uid):
    information = getUserInformation(uid)
    imgLinks = getImageLinks(uid, 1)
    if isGreaterThan(information, 500):
        for link in imgLinks:
            print link
        for k, v in information.items():
            print k, ':', v
    else:
        print 'no'
    print

Thread(target=main, args=(1774543811, )).start()
Thread(target=main, args=(1075567392, )).start()
Thread(target=main, args=(5447809712, )).start()
