import sqlite3
from NewsParser import NewsParser

def update():
    parser = NewsParser()
    newspack = parser.riaParser()
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    for i in range(len(newspack)):
        #cursor.execute('INSERT INTO News (Title,URL) VALUES ("{}","{}")'.format(newspack[i]["title"],newspack[i]["url"]))
        cursor.execute('UPDATE News SET Title="{}" WHERE ID={}'.format(newspack[i]["title"],i+1))
        cursor.execute('UPDATE News SET URL="{}" WHERE ID={}'.format(newspack[i]["url"],i+1))
    db.commit()
    db.close()
    return 0

def show():
    data_news = []
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute('SELECT Title,URL FROM News')
    data = cursor.fetchall()
    for i in range(len(data)):
        data_news.append({'title':data[i][0],'url':data[i][1]})
    db.commit()
    db.close()
    return data_news