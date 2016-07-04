#!/usr/bin/env python
# coding:utf-8
import requests as re
import numpy
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
    'Cookie':'SINAGLOBAL=5931281293742.358.1452508282462; __gads=ID=5a36146630fa668e:T=1458825990:S=ALNI_MZh1T3zAKd9ddVKsnokQpH9-GED_g; _ga=GA1.2.1442097102.1458825990; wb_g_minivideo_5447809712=1; wb_bub_hot_2331740335=1; wb_g_minivideo_2331740335=1; myuid=2331740335; wvr=6; wb_bub_hot_5447809712=1; TC-Page-G0=b05711a62e11e2c666cc954f2ef362fb; SSOLoginState=1467532906; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=4265928568177.777.1467532910175; ULV=1467532910258:272:3:1:4265928568177.777.1467532910175:1467424294699; SCF=AlU6pua4h8VAFCCSWk9ptfy9a56Wr8cfJw4pGFS5IKhER1TGEw0f-8VBs3JN-dkUA0kH181489YgEGOOtwlYWSw.; SUB=_2A256fLdKDeTxGeNK71UZ8CfLyj6IHXVZC6-CrDV8PUJbmtAKLVTWkW8PI200aJP_IStbg1ZuxChY0qDFHw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWlXurN77AppfK3I6VNbye25JpX5o2p5NHD95QfShBN1h54S02EWs4DqcjGq0WQqo8E95tt; SUHB=0HTRL-q4uUrol6; ALF=1499065531; TC-V5-G0=866fef700b11606a930f0b3297300d95; WBStore=8ca40a3ef06ad7b2|undefined; TC-Ugrow-G0=5e22903358df63c5e3fd2c757419b456'
}

# Cookie For URL: http://m.weibo.cn/users/-*-UserID-*-
HEADERS_FOR_GET_INFO = {
    'Cookie':'_T_WM=1867af942c92a23704b094e55fbbfadb; ALF=1470210119; SCF=AlU6pua4h8VAFCCSWk9ptfy9a56Wr8cfJw4pGFS5IKhE8EkPUUOqCty3khnptxk4TRzSm7OF4d7gBVikZzFr0UI.; SUB=_2A256fldEDeTxGeNK71UZ8CfLyj6IHXVZgXkMrDV6PUNbktAKLUigkW1u0NCLekCLCmV8873TAtgW51HJ9A..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWlXurN77AppfK3I6VNbye25JpX5KMhUgL.Fo-XShMReh.NeKz2dJLoI7UoesybePi.; SUHB=0BLYOIro2bXNqF; SSOLoginState=1467623188; gsid_CTandWM=4uA7CpOz5c6o1q6dEOpDBmRdTbu'
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
                imgLinks.append(src['pic_ori'].replace('large', 'thumb300'))

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


# Show Image
def showImage(w_title, url):
    rep = re.get(url, stream=True)
    image = numpy.asarray(bytearray(rep.content), dtype='uint8')
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    cv2.imshow("Image", image)
    cv2.waitKey(0)


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
    ls['UID'] = uid
    return ls


# Show Image
def showImage(w_title, url):
    rep = re.get(url, stream=True)
    image = numpy.asarray(bytearray(rep.content), dtype='uint8')
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    cv2.imshow("Image", image)
    cv2.waitKey(delay=3000)

# 1075567392
# 1774543811

def main(uid):
    information = getUserInformation(uid)
    imgLinks1 = getImageLinks(uid, 1)
    imgLinks2 = getImageLinks(uid, 2)
    imgLinks = imgLinks1 + imgLinks2
    if isGreaterThan(information, 500):
        for k, v in information.items():
            print k, ':', v
        for link in imgLinks:
            showImage("Face", link)
    else:
        print 'no'
    print

# Thread(target=main, args=(1774543811, )).start()
# Thread(target=main, args=(1075567392, )).start()
# Thread(target=main, args=(5447809712, )).start()
print getUserFans(1000000002)
