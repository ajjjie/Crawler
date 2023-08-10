import requests
from bs4 import BeautifulSoup
import random
import re
import pandas as pd
import os
from collections import defaultdict


class CharInfo:
    def __init__(self, name, info, bg, rec):
        self.name = name
        self.info = info
        self.bg = bg
        self.rec = rec


class GenshinCrawlerWiki:
    def __init__(self):
        self.ua_list = [
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        ]
        self.base_url = 'https://wiki.biligame.com/ys'
        self.char_url = f'{self.base_url}/角色'
        self.char_names = self._get_char_names()
        self.save_path = 'outputs/'
        self.char_infos = self._get_char_infos()

    def req(self, url):
        headers = {'User-Agent': random.choice(self.ua_list)}
        return requests.get(url=url, headers=headers)

    def _get_char_names(self):
        soup = BeautifulSoup(self.req(self.char_url).text, 'lxml')
        return list(set([x.text for x in soup.find_all(class_='L')]))

    def _get_char_url(self, char):
        if '旅行者' in char:
            if '无' in char:
                url = f'{self.base_url}/旅行者'
            else:
                url = f'{self.base_url}/旅行者/{char[-2]}'
        else:
            url = f'{self.base_url}/{char}'
        return url

    def cli_char(self, char_name):
        url = self._get_char_url(char_name)
        soup = BeautifulSoup(self.req(url).text, 'lxml')
        info = pd.read_html(str(soup.find(class_='poke-bg').
                                find(name='table')))[0].iloc[:, :2].set_index(0).iloc[:,0].fillna('无')
        bg = ''.join(
            [x.text for x in soup.find(class_='col-sm-4').find_all(name='table', class_='wikitable')[1].find_all('td')])
        try:
            rec_tb = [x for x in soup.find_all(name='div', class_='resp-tab-content') if '套装推荐理由' in x.text][0]
        except IndexError:
            rec_tb = \
                [x for x in soup.find_all(name='ul', class_='resp-tabs-list clearfix') if '套装推荐理由' in x.text][0]
        rec = pd.read_html(str(rec_tb))[0].set_index(0).iloc[:, 0].fillna('无')
        char = CharInfo(char_name, info, bg, rec)
        return char

    def _get_char_infos(self):
        char_infos = defaultdict(list)
        for char_name in self.char_names:
            if '旅行者' in char_name or char_name == '派蒙':
                continue
            char = self.cli_char(char_name)
            char_infos[char.info['所在国家']].append(char)
        return char_infos



if __name__ == '__main__':
    cli = GenshinCrawlerWiki()
