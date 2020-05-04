import requests
import time
import sqlite3


class PlacesParse:
    def __init__(self):
        self.key = 'AIzaSyBZ36mXHzroZxoaCdOIQSUL_-bCidW152w'
        self.types = "shop"

    def getPharmacy(self, userId):
        db = sqlite3.connect('C:/Users/goodf/Desktop/qr/database.db')
        cur = db.cursor()
        print(userId)
        cur.execute("SELECT * FROM Users_inf WHERE UserID = {}".format(userId))
        data = cur.fetchall()[0]
        db.close()
        latitude = data[4]
        longitude = data[5]
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
            if len(data) == 3:
                break
        return data
    
    def getShop(self, userId):
        db = sqlite3.connect('C:/Users/goodf/Desktop/qr/database.db')
        cur = db.cursor()
        cur.execute("SELECT * FROM Users_inf WHERE UserID = {}".format(userId))
        data = cur.fetchall()[0]
        db.close()
        latitude = data[4]
        longitude = data[5]
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
            if len(data) == 3:
                break
        return data
