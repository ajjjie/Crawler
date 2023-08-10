import requests
from bs4 import BeautifulSoup as be
import random
import re
from collections import defaultdict


class GenshinCrawlerOfficial:
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
        self.char_urls = [
            "https://ys.mihoyo.com/content/ysCn/getContentList?pageSize=20&pageNum=1&order=asc&channelId=150"
            , "https://ys.mihoyo.com/content/ysCn/getContentList?pageSize=20&pageNum=1&order=asc&channelId=151"
            , "https://ys.mihoyo.com/content/ysCn/getContentList?pageSize=20&pageNum=1&order=asc&channelId=324"
            , "https://ys.mihoyo.com/content/ysCn/getContentList?pageSize=20&pageNum=1&order=asc&channelId=350"
        ]
        self.char_data = self._get_char_data()

        self.cities = ['蒙德','璃月','稻妻','须弥']
        self.city_url = 'https://ys.mihoyo.com/main/map'
        self.place_data = self._get_places()

    def req(self, url):
        headers = {'User-Agent': random.choice(self.ua_list)}
        return requests.get(url=url, headers=headers)

    def char_query(self, char_name):
        json = self.char_data[char_name]
        for key, value in json.items():
            if key == "音频":
                for keys, values in json[key].items():
                    print(f"{keys}：{values}")
            else:
                print(f"{key}：{value}")

    def _get_char_data(self):
        chars_dict = {}
        for url in self.char_urls:
            req = self.req(url)
            js = req.json()['data']
            jslist = self.char_data(js)
            for json in jslist:
                chars_dict[json['角色名字']] = json
        return chars_dict

    def char_data(self, js):
        _return_ = []
        for key in js['list']:
            ext = key["ext"]
            data = {key['title']: {
                "角色ICON": ext[0]["value"][0]["url"],
                "电脑端立绘": ext[1]["value"][0]["url"],
                "手机端立绘": ext[15]["value"][0]["url"],
                "角色名字": key['title'],
                "角色属性": ext[3]["value"][0]["url"],
                "角色语言": ext[4]["value"],
                "声优1": ext[5]["value"],
                "声优2": ext[6]["value"],
                "简介": be(ext[7]["value"], "lxml").p.text.strip(),
                "台词": ext[8]["value"][0]["url"],
                "音频": {
                    ext[9]["value"][0]["name"]: ext[9]["value"][0]["url"],
                    ext[10]["value"][0]["name"]: ext[10]["value"][0]["url"],
                    ext[11]["value"][0]["name"]: ext[11]["value"][0]["url"],
                    ext[12]["value"][0]["name"]: ext[12]["value"][0]["url"],
                    ext[13]["value"][0]["name"]: ext[13]["value"][0]["url"],
                    ext[14]["value"][0]["name"]: ext[14]["value"][0]["url"],
                },
            }
            }
            _return_.append(data[key['title']])
        return _return_

    def _get_places(self):
        text = self.req(self.city_url).text
        start_points = []
        for city in self.cities:
            start_points.append(text.find(city))
        start_points.append(text.find('注视历史的变迁。')+10)
        places_dict = defaultdict(dict)
        for i,city in enumerate(self.cities):
            city_txt = text[start_points[i]+2:start_points[i+1]]
            places = [re.sub('[^\u4e00-\u9fa5]+', '', x) for x in re.findall(r'E[\u4e00-\u9fa5]+\\', city_txt)]
            places.insert(0,city)
            describes = [re.sub('[^\u4e00-\u9fa5。，]+', '', x) for x in re.split(r'E[\u4e00-\u9fa5]+\\', city_txt)]
            for place,desc in zip(places,describes):
                places_dict[city][place] = desc
        return places_dict

    def place_query(self, place):
        for d in self.place_data.values:
            if d.get(place):
                info = d[place]
                print(info)
                return info
        print('不存在此地点')



if __name__ == '__main__':
    cli = GenshinCrawlerOfficial()
    cli.char_query('纳西妲')
    cli.place_query('化城郭')
    print(cli.place_data)
    print(cli.char_data)
