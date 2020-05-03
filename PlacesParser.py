import requests
import time


class PlacesParse:
    def __init__(self):
        self.key = 'AIzaSyBZ36mXHzroZxoaCdOIQSUL_-bCidW152w'
        self.types = "shop"

    def getPharmacy(self, latitude, longitude):
        name = "pharmacy"
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius=200&types={}&name={}&key={}".format(latitude, longitude, self.types, name, self.key)
        data = requests.get(url)
        print(url)
        response = data.json()['results']
        data = []
        for ph in response:
            data.append(
                {
                    'name':ph['name'],
                    'open_now':ph['opening_hours']['open_now'],
                    'latutide':ph['geometry']['location']['lat'],
                    'latutide':ph['geometry']['location']['lng'],
                }
            )
        return data
    
    def getShop(self, latitude, longitude):
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
                    'open_now':sh['opening_hours']['open_now'],
                    'latutide':sh['geometry']['location']['lat'],
                    'latutide':sh['geometry']['location']['lng'],
                }
            )
        return data