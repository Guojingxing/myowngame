#https://wenku.baidu.com/browse/getbcsurl?doc_id=bb51530e4a7302768e9939af&pn=1&rn=99999&type=ppt&callback=jQuery110104256346361712908_1545049106593&_=1545049106594
import re
import os
import urllib.request
import requests
import json
#url = "https://wenku.baidu.com/browse/getbcsurl?doc_id=bb51530e4a7302768e9939af&pn=1&rn=99999&type=ppt&callback=jQuery110104256346361712908_1545049106593&_=1545049106594"
#data = requests.get(url).text
#jpglist = re.findall('https:\/\/wkretype.bdimg.com\/retype\/zoom\/bb51530e4a7302768e9939af?pn=(.*?)",', data, re.S)
a = []
with open("D://new.json", "r") as f:
    load = json.load(f)
    for i in range(184):
        a.append(load["list"][i]['zoom'])

root = "D://pics//"
for i in range(184):
    path = root +"%d"%i+ '.jpg'
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(a[i])
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print("文件保存成功")
        else:
            print("文件已存在")
    except:
        print("爬取失败")
