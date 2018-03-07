import re
import requests
from bs4 import BeautifulSoup
from functions import change_ip, log
from api import api


class Movie:
    def __init__(self, information):
        self.title = information['title'].replace('"', "'")
        self.id = information['id']
        self.dircetors = '/'.join(information['directors']).replace('"', "'")
        self.casts = '/'.join(information['casts']).replace('"', "'")
        self.image = information['cover']
        self.rate = information['rate'] if len(information['rate']) != 0 else 0
        self.star = information['star'] if len(information['star']) != 0 else 0
        self.url = information['url']
        try:
            content = requests.get(api[1] + self.id).text
        except (ConnectionRefusedError,ConnectionError):        #检测连接是否被拒绝
            log('连接被拒绝 切换ip', 2)
            change_ip()
            content = requests.get(api[1] + self.id).text
        if '检测到' in str(content) or '#info' not in str(content):  # 检测ip是否被ban
            log('ip 被ban 切换ip', 2)
            change_ip()
            content = requests.get(api[1] + self.id).text
        soup = BeautifulSoup(content, "html.parser")
        self.type = '/'.join(
            re.findall('[\u4e00-\u9fa5]{2}', str(soup.find_all('span', attrs={'property': "v:genre"})))).replace('剧情/',
                                                                                                                 '')
        try:
            self.date = soup.find('span', attrs={'property': 'v:initialReleaseDate'}).text
        except AttributeError:
            self.date = '--'
        try:
            self.plot = str(next(soup.find('span', attrs={'property': 'v:summary'}).stripped_strings)).replace('"', "'")
        except (AttributeError, StopIteration):
            self.plot = '--'
        try:
            self.runtime = re.findall(r'片长: \d+分钟|片长: \d+分|片长: \d+min|片长: \d+ 分钟|片长: \d+ 分|片长: \d+ min',
                                      soup.select_one('#info').text)[0][3:]
        except(IndexError, AttributeError):
            self.runtime = '--'
        try:
            self.screenwriter = soup.select('.attrs')[1].text.replace('"', "'")
        except IndexError:
            self.screenwriter = '--'
