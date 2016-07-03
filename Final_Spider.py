#!/usr/bin/env python
# coding:utf-8
import requests as re
import re as R
import time
import os
import Image
import cv2
from threading import Thread
from bs4 import BeautifulSoup as bs
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


# HTTP Request Header
HEADERS = {
    'Cookie':'_T_WM=1867af942c92a23704b094e55fbbfadb; ALF=1470016285; SCF=AlU6pua4h8VAFCCSWk9ptfy9a56Wr8cfJw4pGFS5IKhEm_2HWqf9Qg8D6Wi2jQ3MhTN5luzifKYsq4ZbbALWGD0.; SUB=_2A256fMlvDeTxGeNK71UZ8CfLyj6IHXVZntcnrDV6PUNbktANLW2nkW1WRKGoyuGFLyILiETsh5IOw48dUA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWlXurN77AppfK3I6VNbye25JpX5KMhUgL.Fo-XShMReh.NeKz2dJLoI7UoesybePi.; SUHB=0k1yTQu_RVkCTM; SSOLoginState=1467529535; gsid_CTandWM=4uwFCpOz5G94piRyvJy9qmRdTbu; M_WEIBOCN_PARAMS=featurecode%3D20000181%26luicode%3D10000011%26lfid%3D103003index1075567392%26fid%3D103003index1075567392_-_photo_all_l%26uicode%3D10000012'
}

# Get User Image Links, Return A List
def getImageLinks(url, headers=HEADERS):
    reponse = re.get(url, headers=headers)
    time.sleep(3)

    content = reponse.content.replace('\\', '')


def getUserInformation(uid, headers=HEADERS):
    information = {}

    url = "http://m.weibo.cn/page/card?itemid=100505%d_-_WEIBO_INDEX_PROFILE_APPS&callback=_1467532491343_4&retcode=6102" % uid
    reponse = re.get(url, headers=headers)

    content = reponse.content.replace('\\', '')
    data = json.loads(content[17:-1])
    following = data['apps'][2]['count'].split('u')
    fans = data['apps'][3]['count'].split('u')

    if len(fans) > 1:
        if fans[1] == '4ebf':
            information['FANS'] = fans[0] + '00000000'
        elif fans[1] == '4e07':
            information['FANS'] = fans[0] + '0000'
    else:
        information['FANS'] = fans[0]

    information['UID'] = uid

    return information


def main(uid):
    userInfo = getUserInformation(uid)
    print userInfo['UID']
    if int(userInfo['FANS']) > 500:
        os.system("echo %d >> user.txt" % uid)

judge = False
for uid in range(1000000000, 2000000000):
    Thread(target=main, args=(uid,)).start()
