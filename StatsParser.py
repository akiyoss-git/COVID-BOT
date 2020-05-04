import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fuzzywuzzy import fuzz
import re
import json
from UnicodeCleaner import UCleaner
import sqlite3
import transliterate
import time


class StatsParser():
    def __init__(self):
        pass

    def get_data(self, id):
        db = sqlite3.connect('C:/Users/goodf/Desktop/qr/database.db')
        cur = db.cursor()
        cur.execute("SELECT City FROM Users_inf WHERE UserID = {}".format(id))
        location = cur.fetchall()[0][0]
        db.close()
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
        dic = {
                'title': 'Россия',
                'code': 0,
                'is_city': 0,
                'coord_x': 0,
                'coord_y': 0,
                'sick': 0,
                'healed': 0,
                'died':0,
                'sick_incr':0,
                'healed_incr':0,
                'died_incr':0
            }
        recommendStats = []
        for s in stats:
            if fuzz.partial_ratio(transliterate.translit(s['title'], reversed=True), location) > 99:
                recommendStats.append(s)
            dic['sick'] += int(s['sick'])
            dic['healed'] += int(s['healed'])
            dic['died'] += int(s['died'])
            dic['sick_incr'] += int(s['sick_incr'])
            dic['healed_incr'] += int(s['healed_incr'])
            dic['died_incr'] += int(s['died_incr'])
        recommendStats.append(dic)
        return recommendStats
    
    def sendStat(self):
        db = sqlite3.connect('C:/Users/goodf/Desktop/qr/database.db')
        cur = db.cursor()
        cur.execute('SELECT UserID FROM Users_inf WHERE MailingStats = \'True\'')
        ids = cur.fetchall()[0]
        full = []
        for id in ids:
            data = self.get_data(id)
            full.append(
                {
                    'id': id,
                    'data': data
                }
            )
        return full