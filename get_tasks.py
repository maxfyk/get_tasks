"""This service allows to get new tasks form database"""
import os
import sys
import time
import MySQLdb
from rq import Worker, Queue, Connection
from methods.connection import get_redis, get_cursor

r = get_redis()

def get_tasks(type = "ALL", col="", value=""):
    """Returns new tasks from databse (table tasks)"""
    cursor, db = get_cursor()
    if not cursor or not db:
        # log that failed getting cursor
        return False
    q = "SELECT * FROM tasks "
    if type is not None:
        if type == "WHERE" and col and value:
            value = value.replace(";", "")
            value = value.replace("'", "''")
            q += f"""WHERE {col} = '{value}'"""
        elif type == "ALL":
            pass
        else:
            return False
    try:
        cursor.execute(q)
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
