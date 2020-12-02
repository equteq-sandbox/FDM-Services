from db.DatabaseConnector import getConnection
from db.DBUtils import performDBUpdate, retrieveDBQuery
from models.User import User
import json



def addUser(params):
    try:
        user = User(params.get('user_name'), params.get('first_name'), params.get('last_name'), params.get('email'), params.get('phone_number'))
        print(user.__dict__)
        
        sql = "INSERT INTO [User] (userName, firstName, lastName, email, phoneNumber, isValidated) \
            VALUES(?, ?, ?, ?, ?, 0)"
        dbConn = getConnection();
        update = performDBUpdate(dbConn, sql, user.user_name, user.first_name, user.last_name, user.email, user.phone_number)
        return True # db update successful when the function reaches this point
    except:
        return False # some kind of error in the db udpate process caused an exception


def getUser(uid):
    sql = "SELECT * FROM [User] WHERE UserId=?" # use a prepared statement here
    dbConn = getConnection();
    results = retrieveDBQuery(dbConn, sql, uid) 
    if results:
        userInfo = results[1:6] # since our user model class does not contain all the attributes in the db
        user = User(*userInfo)
        return user

    return None
