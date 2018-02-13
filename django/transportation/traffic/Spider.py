# !/usr/bin/python3

import urllib.request
import urllib.error
import requests
import re
import json
import datetime
import pytz
import os
import time

class Spider:
    def __init__(self):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.refer = 'https://catalog.data.gov/dataset/chicago-traffic-tracker-congestion-estimates-by-segments-0b9d7'
        self.headers = {'User-Agent': self.user_agent, 'Referer': self.refer}
        self.session = requests.Session()


    def getContent(self):
        try:
            url = 'https://catalog.data.gov/dataset/chicago-traffic-tracker-congestion-estimates-by-segments-0b9d7'
            # 获取页面内容
            pageContent = self.session.get(url, headers=self.headers).text
            # 转换编码
            return pageContent
        except (urllib.error.URLError) as e:
            if hasattr(e, 'reason'):
              print(u'连接失败，原因：', e.reason)
              return None

    def getUrlFromContent(self):
        pageContent = self.getContent()

        if not pageContent:
            print(u'页面加载失败')
            return None

        pattern = re.compile('<li.*?distribution.*?<a.*?contentUrl.*?<span.*?>JSON</span>.*?<div.*?>(.*?)</div>', re.S)
        aitems = re.findall(pattern, pageContent)

        urlpattern = re.compile('<a.*?"(.*?)"', re.S)
        items = re.findall(urlpattern, aitems[0])

        if not items:
            return None

        return items[0]

    def getJSONContent(self):
        url = self.getUrlFromContent()

        if not url:
            print(u'链接获取失败')
            return None

        content = self.session.get(url).text
        print(u'get content...')
        # file = open('jsondata.json', 'w')
        # file.write(str(content))
        self.saveFile(content)

    def saveFile(self, content):
        print(u'try to save')
        jsonObject = json.loads(content)
        items = jsonObject['data']

        storeList = []
        currentTime = datetime.datetime.now(pytz.timezone('US/Central'))
        currentTime = currentTime.replace(tzinfo=None)

        for item in items:
            itemtime = item[21].split('.')[0]
            t = datetime.datetime.strptime(itemtime, "%Y-%m-%d %H:%M:%S")
            if (currentTime - t).days == 0 and (currentTime - t).seconds < 3600:
                storeList.append(item)

        filePath = self.filePathCurrentTime()
        file = open(filePath, 'w')

        try:
            for item in storeList:
                json_str = json.dumps(item)
                file.write(str(json_str) + '\n')

            print(u'success to save')
        except (IOError) as e:
            print('fail to open file')
        finally:
            file.close()


    def filePathCurrentTime(self):
        currentTime = datetime.datetime.now(pytz.timezone('US/Central'))
        basepath = os.path.dirname(__file__)
        filepath = basepath + '/data/' + str(currentTime.year) + '/' + str(currentTime.month) + '/' + str(currentTime.day)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filepath = filepath + '/' + str(currentTime.hour) + '.json'
        return filepath



    def start(self):
        try:
            while (True):
                print(u'check if there has data avaliable')
                try:
                    self.getJSONContent()
                except requests.exceptions.ConnectionError as e:
                    print(u'failed to connect the host')
                print(u'wait for next time...')
                time.sleep(3000)
        except (ConnectionResetError) as e:
            print(e)
