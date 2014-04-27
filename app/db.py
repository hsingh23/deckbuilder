from app import app
c = app.config
import MySQLdb
from MySQLdb.cursors import DictCursor


def get_connection():
    if "connection" in c:
        return c["connection"]
    else:

        connection = MySQLdb.connect(host=c["DATABASE_HOST"], user=c[
                                     "DATABASE_USER"], passwd=c["DATABASE_PASSWORD"], db=c["DATABASE_DATABASE"])
        app.config["connection"] = connection
        return connection


def get_cursor():
    return get_connection().cursor()


def make_dicts(cursor, rows):
    return [dict((cursor.description[idx][0], value) for idx, value in enumerate(row)) for row in rows]

def query_one(query, args):
    cursor = get_cursor()
    cursor.execute(query, args)
    result = cursor.fetchone()
    cursor.close()
    return result

def query_all(query, args):
    cursor = get_cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    cursor.close()
    return result

