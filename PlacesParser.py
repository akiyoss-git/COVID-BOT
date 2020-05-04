import requests
import time
import sqlite3


class PlacesParse:
    def __init__(self):
        self.key = 'AIzaSyBZ36mXHzroZxoaCdOIQSUL_-bCidW152w'
        self.types = "shop"

    def getPharmacy(self, userId):
        db = sqlite3.connect('database.db')
        cur = db.cursor()
        cur.execute("SELECT * FROM Users WHERE Id = {}".format(userId))
        data = cur.fetchall()[0]
        db.close()
        latitude = data[2]
        longitude = data[3]
        name = "pharmacy"
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius=100&types={}&name={}&key={}".format(latitude, longitude, self.types, name, self.key)
        data = requests.get(url)
        response = data.json()['results']
        data = []
        for ph in response:
            data.append(
                {
                    'name':ph['name'],
                    'url': f"""https://www.google.com/maps/search/?api=1&query={ph['geometry']['location']['lat']},{ph['geometry']['location']['lng']}"""
                }
            )
        return data
    
    def getShop(self, userId):
        db = sqlite3.connect('database.db')
        cur = db.cursor()
        cur.execute("SELECT * FROM Users WHERE Id = {}".format(userId))
        data = cur.fetchall()[0]
        db.close()
        latitude = data[2]
        longitude = data[3]
        name = "general+store"
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius=200&types={}&name={}&key={}".format(latitude, longitude, self.types, name, self.key)
        data = requests.get(url)
        print(url)
        response = data.json()['results']
        data = []
        for sh in response:
            data.append(
                {
                    'name':sh['name'],
                    'url': f"""https://www.google.com/maps/search/?api=1&query={sh['geometry']['location']['lat']},{sh['geometry']['location']['lng']}"""
                }
            )
        return data

p = PlacesParse()
print(p.getPharmacy(752446250))