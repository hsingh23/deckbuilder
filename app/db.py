from app import app
c = app.config
import MySQLdb
def get_connection():
    if "connection" in c:
        return c["connection"]
    else:
        connection = MySQLdb.connect(host=c["DATABASE_HOST"], user=c[
                                     "DATABASE_USER"], passwd=c["DATABASE_PASSWORD"], db=c["DATABASE_DATABASE"])
        app.config["connection"] = connection
        return connection
