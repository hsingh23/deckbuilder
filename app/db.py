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


def get_dict_connection():
    if "dict_connection" in c:
        return c["dict_connection"]
    else:

        connection = MySQLdb.connect(host=c["DATABASE_HOST"], user=c[
                                     "DATABASE_USER"], passwd=c["DATABASE_PASSWORD"], db=c["DATABASE_DATABASE"], cursorclass=DictCursor)
        app.config["dict_connection"] = connection
        return connection

def get_dict_cursor():
	return get_dict_connection().cursor()