"""This service allows to get new tasks form database"""
import os
import sys
import time
import MySQLdb
from rq import Worker, Queue, Connection
from methods.connection import get_redis, get_cursor


def get_tasks():
    cursor, db = get_cursor()
    if not cursor or not db:
        # log that failed getting cursor
        return False
    """Returns new tasks from databse (table tasks)"""
    # insert some tasks for testing
    try:
        cursor.execute("truncate tasks")
        cursor.execute("INSERT INTO  tasks (id, channel_id, added_on) VALUES   (1, 'UCXuqSBlHAE6Xw-yeJA0Tunw', NOW())")
        cursor.execute("INSERT INTO  tasks (id, channel_id, added_on) VALUES   (2, 'UCdBK94H6oZT2Q7l0-b0xmMg', NOW())")
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
    time.sleep(5)
    r = get_redis()
    q = Queue('get_tasks', connection=r)
    with Connection(r):
        worker = Worker([q], connection=r, name='get_tasks')
        worker.work()
