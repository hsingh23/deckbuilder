def get_cursor():
    from app import app
    c = app.config
    if "connection" in c:
        return c["connection"].cursor()
    else:
        import MySQLdb
        connection = MySQLdb.connect(host=c["DATABASE_HOST"], user=c[
                                     "DATABASE_USER"], passwd=c["DATABASE_PASSWORD"], db=c["DATABASE_DATABASE"])
        app.config["connection"] = connection
        return connection.cursor()
