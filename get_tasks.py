"""This service allows to get new tasks form database"""
import os
import sys
import time
import MySQLdb
from rq import Worker, Queue, Connection
from methods.connection import get_redis, get_cursor

r = get_redis()

def get_tasks():
    cursor, db = get_cursor()
    if not cursor or not db:
        # log that failed getting cursor
        return False
    """Returns new tasks from databse (table tasks)"""
    # insert some tasks for testing
    try:
        cursor.execute("truncate tasks")
        cursor.execute("INSERT INTO  tasks (id, channel_id, added_on) VALUES   (1, 'UCngjw6cGfzm6bUIDuhGMntg', NOW())")
        cursor.execute("INSERT INTO  tasks (id, channel_id, added_on) VALUES   (2, 'UC2oSO2sCto3bW0hvjXYMMiA', NOW())")
        db.commit()
    except Exception as e:
        print(e)
    try:
        cursor.execute("SELECT * FROM tasks")
    except MySQLdb.Error as error:
        print(error)
        # Log
        return False
        # sys.exit("Error:Failed getting new tasks from database")
    data = cursor.fetchall()
    cursor.close()
    return data


if __name__ == '__main__':
    q = Queue('get_tasks', connection=r)
    with Connection(r):
        worker = Worker([q], connection=r, name='get_tasks')
        worker.work()
