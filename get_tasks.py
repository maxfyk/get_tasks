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
        # Test my channel only
        cursor.execute("INSERT INTO  tasks (channel_id, added_on) VALUES   ('UCngjw6cGfzm6bUIDuhGMntg', NOW())")
        cursor.execute("INSERT INTO  tasks (channel_id, added_on) VALUES   ('UC2oSO2sCto3bW0hvjXYMMiA', NOW())")
        cursor.execute("INSERT INTO  tasks (channel_id, added_on) VALUES   ('UCf34x101_ycTUjAQ2SxMRWA', NOW())")
        cursor.execute("INSERT INTO  tasks (channel_id, added_on) VALUES   ('UC7B-nApg76kClvW-YBYezQQ', NOW())")
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
