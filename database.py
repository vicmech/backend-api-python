import logging
import mysql.connector
from mysql.connector import Error as E

logging.basicConfig(filename='connection.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def getConnection():
    try:
        con = mysql.connector.MySQLConnection(
            host ="localhost",
            port = 3306,
            user="root",
            password="root",
            database="delivery-cases-db"
        )
        if con.is_connected():
            print('Connection established')
        return con
    except E:
        logging.error('Connection failed: ' + E)

def closeConnection(con):
    con.close()
    print('Connection closed')
    logging.info('Connection closed')