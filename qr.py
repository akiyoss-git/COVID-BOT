import json
from decimal import Decimal
import os
import sqlite3
import googlemaps
import requests

from geopy.geocoders import Nominatim


def recive_qr (UserID):
    db = sqlite3.connect("C:/Users/goodf/Desktop/qr/database.db")
    cursor = db.cursor()
    cursor.execute('SELECT City FROM Users_inf WHERE UserID = "{}"'.format(UserID))
    City = cursor.fetchall()[0]
    print(City)
    cursor.execute('SELECT URL FROM Cities_qr WHERE City = "{}"'.format(City[0]))
    URL = cursor.fetchall()[0][0]
    db.commit()
    db.close()
    return URL

def record_City (map_URL, userID):
    data = map_URL.split('=')
    coord = data[2].split(',')
    print (coord[0],coord[1])
    db = sqlite3.connect("C:/Users/goodf/Desktop/qr/database.db")
    cursor = db.cursor()
    value = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?latlng={coord[0]},{coord[1]}&key=AIzaSyBZ36mXHzroZxoaCdOIQSUL_-bCidW152w').json()
    City = value['results'][0]['address_components'][2]['long_name']
    cursor.execute('UPDATE Users_inf SET City = "{}" WHERE UserID = "{}"'.format(City,userID))
    cursor.execute('UPDATE Users_inf SET Latitude = {} WHERE UserID = "{}"'.format(float(coord[0]),userID))
    cursor.execute('UPDATE Users_inf SET Longitude = {} WHERE UserID = "{}"'.format(float(coord[1]),userID))
    db.commit()
    db.close()
    return 0

def check_City (userID):
    db = sqlite3.connect("C:/Users/goodf/Desktop/qr/database.db")
    cursor = db.cursor()
    cursor.execute('SELECT City FROM User_inf WHERE User="{}"'.format(userID))
    if not cursor.fetchall() == []:
        db.commit()
        db.close()
        return 0
    else:
        db.commit()
        db.close()
        return 1



