# -*- coding:utf-8 -*-

'''
created by kygeng
'''

import requests
import json
from bs4 import BeautifulSoup
from sys import argv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6"
}

handleSS = requests.Session()
hostUrl = "https://www.66ss.ml"

def writeFile(fileName, fileContent):
    with open(fileName, 'w') as file:
        file.write(fileContent)

def login(userName, userPasswd):

    # 设置请求头和参数
    params = {"email": userName, "passwd": userPasswd}

    global headers
    global handleSS
    global hostUrl
    loginUrl = hostUrl + "/auth/login"

    # 发起模拟登录
    response = handleSS.post(loginUrl, headers=headers, data=params, verify=False)
    respData = json.loads(response.text)
    if response.status_code == 200 and respData["ret"] == 1:
        return True
    else:
        return False

# 获取节点状态列表
def getNodeList():
    global headers
    global hostUrl
    nodeListUrl = hostUrl + "/user/node"

    response = handleSS.get(nodeListUrl, headers=headers, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text)
        for tag in soup.find_all("div", class_="tile tile-collapse"):
            content = tag.find("div", class_="avatar avatar-sm").find("span").string
            for string in tag.find("div", class_="tile-inner").find("div").strings:
                content += repr(string)
            print(content)
            print("----------------------------------------------------------------------------")

# 下载最新的节点配置文件
def downLoadNode():
    global headers
    global hostUrl
    nodeDownLoadUrl = hostUrl + "/user/getpcconf?without_mu=0"

    response = handleSS.get(nodeDownLoadUrl, headers=headers, verify=False)
    if response.status_code == 200:
        fileName = "66ss-gui-config.json"
        if hostUrl == "https://www.66ssplus.ml":
            fileName = "66ssplus-gui-config.json"
        writeFile(fileName, response.text)
        print("download node list success")

if __name__ == '__main__':
    print("1. www.66ss.ml")
    print("2. www.66ssplus.ml")
    server = input("Please choose server:")
    if server == '2':
        print("you choose server 2")
        hostUrl = "https://www.66ssplus.ml"
    else:
        print("you choose server 1")

    ret = login("","")
    if ret == True:
        print('login success')
        getNodeList()
        downLoadNode()
    else:
        print('error login failed')