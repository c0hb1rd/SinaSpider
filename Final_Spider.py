#!/usr/bin/env python
# coding:utf-8
import requests
import numpy
import os
import cv2
from bs4 import BeautifulSoup
import sys
import json
# import re as R
# import time
# import Image
# from threading import Thread


## URL For Get User Image Links, JSON Page
# http://m.weibo.cn/page/json?containerid=103003index|-*-UserID-*-|_-_photo_all_l&page=1&retcode=6102, e.g: 1075567392
## End

## URL For Get User Information, HTML Page
# http://m.weibo.cn/users/|-*-UserID-*-|?retcode=6102, e.g: 1075567392
## End

## URL For Get User Fans, JSON Page
# http://m.weibo.cn/page/card?itemid=100505|-*-UserID-*-|_-_WEIBO_INDEX_PROFILE_APPS&callback=_1467532491343_4&retcode=6102, e.g: 1075567392
## End

# Set Default Encode
reload(sys)
sys.setdefaultencoding('utf-8')

# Default Cookie
HEADERS = {
    'Cookie':''
}

# Cookie For Get User Information
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
            reponse = requests.get(url, headers=headers)
            reponse.close()

            if reponse:
                content = reponse.content.replace('\\', '')
            data = json.loads(content)

            for src in data['cards'][0]['card_group'][0]['pics']:
                imgLinks.append(src['pic_ori'].replace('large', 'thumb300')) # Large Type Picture is too Big

            return imgLinks
        except:
            continue


# Download Image
def downloadImage(imgURL, path, filename):
    while True:
        try:
            reponse = requests.get(imgURL, stream=True)
            with open(path + filename, 'wb') as f:
                for buff in reponse.iter_content(chunk_size=1024):
                    if buff:
                        f.write(buff)
                        f.flush()
            break
        except:
            continue


# Get User Fans Total, Return Int
def getUserFans(uid, headers=HEADERS):
    url = "http://m.weibo.cn/page/card?itemid=100505%d_-_WEIBO_INDEX_PROFILE_APPS&callback=_1467532491343_4&retcode=6102" % uid
    reponse = requests.get(url, headers=headers)
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


# Get User Information, Return Dict
def getUserInformation(uid, headers=HEADERS_FOR_GET_INFO):
    url = "http://m.weibo.cn/users/%d?retcode=6102" % uid
    reponse = requests.get(url, headers=HEADERS_FOR_GET_INFO)
    reponse.close()

    content = BeautifulSoup(reponse.content.replace("\\", '').replace("rn", ""), "lxml")
    content = content.find_all('div', 'item-info-page')

    info = {}
    for v in content:
        key = str(v.find('span'))[6:-7]
        value = str(v.find('p'))[3:-4]
        if key == '备注':
            continue
        elif key == '勋章':
            continue
        elif key[-12:] == '微博认证':
            key = key[-12:]
        info[key] = value
    info['UID'] = uid

    return info


# Show Image
def showImage(w_title, path, delay=2000):
    image = ''
    # Loads Image From URL
    if path[:7] == 'http://':
        rep = requests.get(url, stream=True)
        image = numpy.asarray(bytearray(rep.content), dtype='uint8')
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # Loads Image From Disk
    else:
        image = cv2.imread(path)
    cv2.imshow(w_title, image)
    cv2.waitKey(delay=delay)


def main(uid):
    userFans = getUserFans(uid)
    # If User Fans Greater Than 500, Run It!
    if userFans >= 500:
        path = os.path.abspath('.') + '/Sina_' + str(uid) + '/'
        if os.path.exists(path) != True:
            os.mkdir(path)
        else:
            print '[*]User ' + str(uid) + " is exists."
            return

        information = getUserInformation(uid)
        information['粉丝'] = userFans
        imgLinks = getImageLinks(uid, 1)

        # Save User Information To Disk
        with open(path + 'userInfo.txt', 'w') as file:
            for k, v in information.items():
                line =  str(k) + ':' + str(v)
                file.writelines(line + "\n")
            file.close()

        # Detect Images whether Has Faces And Then Save It To Disk
        count = 1
        for link in imgLinks:
            filename = str(count) + '.jpg'
            # print '[*]Downloading ' + link + '......'
            downloadImage(link, path, filename)
            # print '[*]Downloaded ' + link
            if detectFaces(path + filename):
                showImage(str(uid), path + filename)
            else:
                os.system('rm ' + path + filename)
            count += 1

        print '[*]Process user ' + str(uid) + " completion."
    else:
        print "[*]User %d fans smaller than 500." % uid


# Thread(target=main, args=(1774543811, )).start()
# Thread(target=main, args=(1075567392, )).start()
# Thread(target=main, args=(5447809712, )).start()

## Testing User List
# 1075567392 Fans Greater Than 500
# 1774543811 Fans Greater Than 500
# 5447809712 Fans Smallter Than 50
# 1000000000 not exists
# 1000000002 Fans Smallter Than 10
## End
if __name__ == '__main__':
    uidList = [1075567392, 1774543811, 5447809712, 1000000000, 1000000002]
    for uid in uidList:
        main(uid)
