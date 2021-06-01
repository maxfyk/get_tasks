"""This service allows to get new tasks form database"""
import os
import sys
import time
import MySQLdb
from redis import Redis
from rq import Worker, Queue, Connection

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

def get_redis():
    """Returns redis connection"""
    try:
        redis = Redis(host='redis', port=6379)
    except Redis.DoesNotExist as error:
        print(error)
        sys.exit("Error: Faild connecting to redis")
    return redis


def get_tasks():
    cursor = get_cursor()
    """Returns new tasks from databse (table tasks)"""
    try:
        cursor.execute("SELECT * FROM tasks")
    except MySQLdb.Error as error:
        print(error)
        sys.exit("Error:Failed getting new tasks from database")
    data = cursor.fetchall()
    cursor.close()
    return data


if __name__ == '__main__':
    time.sleep(5)
    r = get_redis()
    q = Queue('get_tasks', connection=r)
    with Connection(r):
        worker = Worker([q], connection=r, name='get_tasks')
        worker.work()
