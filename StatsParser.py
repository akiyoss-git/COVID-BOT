import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fuzzywuzzy import fuzz
import re
import json
from UnicodeCleaner import UCleaner


class Coronavirus():
    def __init__(self):
        pass

    def get_data(self):
        url = 'https://стопкоронавирус.рф/information/'
        r = requests.get(url)
        if r.ok: # 200  ## 403 404
            html = r.text
        soup = BeautifulSoup(html, 'lxml')
        data=soup.find('cv-spread-overview').get(":spread-data")
        data = data.replace("},{", "}{")
        data = data.replace("]", "")
        data = data.replace("[", "")
        data = UCleaner(data)
        dataset = data.split("}{")
        stats = []
        
        for datas in dataset:
            datas = datas.replace('\"','')
            datas = datas.replace('{','')
            datas = datas.replace('}','')
            full = datas.split(",")
            dic = {
                'title': None,
                'code': None,
                'is_city': None,
                'coord_x': None,
                'coord_y': None,
                'sick': None,
                'healed': None,
                'died':None,
                'sick_incr':None,
                'healed_incr':None,
                'died_incr':None
            }
            for strs in full:
                s = strs.split(":")
                dic[s[0]] = s[1]
            stats.append(dic)
        print(stats)
        return stats