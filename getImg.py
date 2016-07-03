#!/usr/bin/env python
# coding=utf-8
from selenium import webdriver
import time
import sys
import os
import requests
import threading
import codecs
import cv2
import Image


reload(sys)
sys.setdefaultencoding('utf-8')


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

def saveFacees(imageName):
    faces = detectFaces(imageName)
    if faces:
        saveDir = imageName.split('.')[0] + '_faces'
        os.mkdir(saveDir)
        count = 1
        for (x1, y1, x2, y2) in faces:
            fileName = saveDir + "/" +  str(count) + ".jpg"
            Image.open(imageName).crop((x1, y1, x2, y2)).save(fileName)
            count += 1

def downloadImage(imgUrl, path, count):
    while True:
        try:
            r = requests.get(imgUrl, stream=True)
            with open(path, 'wb') as f:
                for buff in r.iter_content(chunk_size=1024):
                    if buff:
                        f.write(buff)
                        f.flush()
            break
        except:
            continue
    print '[*]Download complete(%d)' % count
    if detectFaces(path):
        saveFacees(path)


def saveUserInfomation(information, path):
    with codecs.open(path + '/userInfo.txt', 'w', 'utf-8') as f:
        for k, v in information.items():
            line = str(k) + ':' + str(v)
            f.writelines(line + "\n")

def getUserInformation(client):
    info = {}
    elements = client.find_elements_by_class_name('S_txt1')
    info['Username'] = client.find_element_by_class_name('username').text
    info['Followeing'] = elements[10].text.split('\n')[0]
    info['Fans'] = elements[11].text.split('\n')[0]
    info['Save_Time'] = time.ctime()
    return info

def getImgLink(client):
    #跳转到图片页面
    client.find_elements_by_class_name('S_txt1')[9].click()
    time.sleep(5)
    imgTags = client.find_elements_by_class_name('photo_pict')
    imgLink = []
    for imgSrc in imgTags:
        imgLink.append(imgSrc.get_attribute('src'))
    return imgLink




client = webdriver.Chrome()

for value in range(1774543811, 1774543851):
    try:
        print '[*]Proces:', value
        path = '/home/c01b1rd/Pictures/SinaSpider/' + str(value)
        client.get('http://weibo.com/u/' + str(value))
        time.sleep(6)

        print client.current_url
        if client.current_url[-5] == '10008' or client.current_url == 'http://overseas.weibo.com/' or client.current_url == 'http://weibo.com/sorry?pagenotfound&':
            print 'BOOM'
            time.sleep(3)
            continue
        else:
            try:
                os.mkdir(path)
            except:
                pass
            information = getUserInformation(client)
            information['UserID'] = str(value)
            if int(information['fans']) < 500:
                try:
                    os.rmdir(path)
                except:
                    pass
                continue

            imgLink = getImgLink(client)

            saveUserInfomation(information, path)
            count = 1
            print '[*]Total image:', len(imgLink)
            for image in imgLink:
                threading.Thread(target=downloadImage, args=(image.replace('thumb300', 'large'), path + "/" + str(count) + ".jpg", count)).start()
                count += 1
    except:
        continue

client.close()
print 'Over'
