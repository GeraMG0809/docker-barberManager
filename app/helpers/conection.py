import pymysql

def Connection()-> pymysql.connections.Connection:
    return pymysql.connect(host="barber_manager_db", user='root', password='root', db='barber_manager_db')
