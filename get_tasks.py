"""This service allows to get new tasks form database"""
import os
import sys
import time
import MySQLdb


def get_cursor():
    """Returns database cursor"""
    try:
        mydb = MySQLdb.connect(
            host="database",
            password=os.environ['MYSQL_ROOT_PASS'],
            database='youpar'
        )
    except MySQLdb.Error as error:
        print(error)
        sys.exit("Error: Failed connecting to database")
    return mydb.cursor()

cursor = get_cursor()

def get_tasks():
    """Returns new tasks from databse (table tasks)"""
    # not finished nor tested yet
    try:
        cursor.execute("SELECT * FROM tasks")
    except MySQLdb.Error as error:
        print(error)
        sys.exit("Error:Failed getting new tasks from database")
    return cursor.fetchall()
