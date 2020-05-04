import sqlite3

def add(UserID):
    print('hz')
    db = sqlite3.connect("C:/Users/goodf/Desktop/qr/database.db")
    cursor = db.cursor()
    '''cursor.execute('SELECT ID FROM Users_inf WHERE User = "{}"'.format(UserID))
    data = cursor.fetchall()
    if not data == []:
        db.commit()
        db.close()
        print('ne_ok')
        return('user found')
    else:'''
    cursor.execute('INSERT INTO Users_inf (UserID,Branch) VALUES ("{}","main")'.format(UserID))
    db.commit()
    db.close()
    print('ok')
    return ('user add')


def change_branch(UserID,branch):
    db = sqlite3.connect("C:/Users/goodf/Desktop/qr/database.db")
    cursor = db.cursor()
    cursor.execute('SELECT Branch FROM Users_inf WHERE UserID = "{}"'.format(UserID))
    #data = cursor.fetchall()
    #if not data[0][0] == branch:
    cursor.execute('UPDATE Users_inf SET Branch ="{}"'.format(branch))
    db.commit()
    db.close()
    print('hello')
    return ('ok')
    '''else:
        db.commit()
        db.close()
        print('nope')
        return('nope')'''

def check_branch(UserID):
    db = sqlite3.connect("C:/Users/goodf/Desktop/qr/database.db")
    cursor = db.cursor()
    cursor.execute('SELECT Branch FROM Users_inf WHERE UserID = "{}"'.format(UserID))
    branch = cursor.fetchall()[0][0]
    db.commit()
    db.close()
    return branch

