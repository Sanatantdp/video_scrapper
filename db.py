from sqlalchemy import text
from mysql.connector import Error
from sqlalchemy.orm import sessionmaker
import mysql.connector


def test_mysql_connection1():

    try:

        conn = mysql.connector.connect(
            host='35.213.166.38',
            user='uomheo55eyzgb',
            password='p0t23lim5ogh',
            database='db7uhz37amwvyv'
        )

        if conn.is_connected():
            print("Successfully connected to MySQL Server.")
            return conn, conn.cursor()
        else:
            print('yes')
    except Error as e:
        return f"Error while connecting to MySQL:{e}",
