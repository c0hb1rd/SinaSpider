#URL For Get User Image Links, JSON page
http://m.weibo.cn/page/json?containerid=103003index|-*-UserID-*-|_-_photo_all_l&page=1&retcode=6102, e.g: 1075567392

#URL For Get User Information, HTML Page
http://m.weibo.cn/users/|-*-UserID-*-|?retcode=6102, e.g: 1075567392## End

#URL For Get User Fans, JSON Page
http://m.weibo.cn/page/card?itemid=100505|-*-UserID-*-|_-_WEIBO_INDEX_PROFILE_APPS&callback=_1467532491343_4&retcode=6102, e.g: 1075567392

#Define Function
<ul>
<li><b>Get User Image Links, Return List</b>: getImageLinks(uid, page, headers=HEADERS)</li>
<li><b>Download Image</b>: downloadImage(imgURL, path, filename)</li>
<li><b>Get User Fans Total, Return Int</b>: getUserFans(uid, headers=HEADERS)</li>
<li><b>Detect Image whether Has Faces</b>: detectFaces(imageName)</li>
<li><b>Get User Information, Return Dict</b>: getUserInformation(uid, headers=HEADERS_FOR_GET_INFO)</li>
<li><b>Show Image</b>: showImage(w_title, path, delay=2000)</li>
</ul>

