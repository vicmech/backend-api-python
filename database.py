import mysql.connector
from mysql.connector import Error as E

print('Attempting connection to database...')

try:
    con = mysql.connector.MySQLConnection(
        host ="localhost",
        port = 3306,
        user="root",
        password="root",
        database="ong_database"
    )
    if con.is_connected():
        print('Connected to database successfully')
    else:
        print('Connection to database failed')
except E:
    print(E) 

cursor = con.cursor()

