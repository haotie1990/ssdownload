# -*- coding:utf-8 -*-
'''
created by kygeng
'''

import requests
import json
import os
import sys
import stat

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
}

handleSS = requests.Session()
hostUrl = 'https://www.rbq.buzz'

def writeFile(fileName, fileContent):
    with open(fileName, 'w') as file:
        file.write(fileContent)

def readFile(fileName):
    with open(fileName, 'rt') as file:
        return file.read()

def parseFile(fileName):
    guiConfig = json.loads(readFile('gui-config.json'))
    configs = guiConfig['configs']
    for config in configs:
        cmd = 'sslocal -s {} -p {} -b 127.0.0.1 -l 1080 -k \"{}\" -m \"{}\"'.format(config['server'], config['server_port'], config['password'], config['method'])
        content = '#!/bin/bash\n' + cmd + '\n'
        cmdFileName = config['remarks'] + '.sh'
        writeFile(cmdFileName, content);
        os.chmod(cmdFileName, stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)
    print('Parse success.')

def login(userName, userPasswd):
    params = {'email': userName, 'passwd': userPasswd}
    url = hostUrl + '/auth/login'
    response = handleSS.post(url, headers=headers, data=params)
    if (response.status_code == 200):
        print('Login success, Please waiting for loading gui-config file.')
        urlLoad = hostUrl + '/user/getpcconf?without_mu=0'
        r = handleSS.get(urlLoad)
        fileContent = r.text
        print('Load success, Please waiting for parsing gui-config file.')
        writeFile('gui-config.json',fileContent)
        parseFile('gui-config.json')


if __name__ == '__main__':
    login('', '')