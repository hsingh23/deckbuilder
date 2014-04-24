#!flask/bin/python
if __name__ == "__main__":
    from app import app
    app.run(host='0.0.0.0', port=5000, debug = True)
