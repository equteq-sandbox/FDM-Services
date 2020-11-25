import pyodbc

server = '<server name>'
database = '<db name>'
username = '<user>'
password = '<password>'   
driver= '{ODBC Driver 17 for SQL Server}'


def getConnection():
    print("getting connnection")
    return pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)