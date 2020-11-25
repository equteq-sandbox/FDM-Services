# utility module that allows for separation of actual db query execution from the rest of the code

def performDBUpdate(dbConn, sql, *args):
    try:
        with dbConn as conn:
            with conn.cursor() as cursor:
                execution = cursor.execute(sql, *args) # execution of sql query (parameterization protects against injection attacks)
                dbConn.commit()
        return True # query successful if function gets here
    except:
        return False

def retrieveDBQuery(dbConn, sql, *args):
    try:
        with dbConn as conn:
            with conn.cursor() as cursor:
                execution = cursor.execute(sql, *args) # execution of sql query (parameterization protects against injection attacks)
                row = cursor.fetchone()
            print('db query result: ', row)
        return row # returns row(s) produced from the successfully executed sql query
    except:
        return None

print("test")