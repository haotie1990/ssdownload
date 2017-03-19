'''
created by kygeng
'''

import requests

def writeFile(fileName, fileContent):
    with open(fileName, "w") as file:
        file.write(fileContent)
    print("write success")

def login(userName, userPasswd):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6"
    }
    params = {"email":userName,"passwd":userPasswd}
    url = "https://www.66ss.ml/auth/login"
    sss = requests.Session()
    response = sss.post(url, headers=headers, data=params)
    if (response.status_code == 200):
        urlLoad = "https://www.66ss.ml/user/getpcconf?without_mu=0"
        r = sss.get(urlLoad)
        fileContent = r.text
        print("load success")
        writeFile("gui-config.json",fileContent)


login("","")
