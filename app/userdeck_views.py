from db import get_cursor, query_one, query_all
from simplejson import dumps as to_json
from flask import request
from app import app


@app.route('/user/<google_id>', methods=["GET"])
def get_user_deck(google_id):
    try:
        return to_json(query_all("""SELECT deck_id, json FROM UserDecks WHERE google_id""", google_id))
    except:
        return '{"error":"not found"}'


@app.route('/user/', methods=["POST"])
def save_user_deck():
    try:
        json = request.args["json"]
        google_id = request.args["google_id"]
        cursor = get_cursor()
        cursor.execute(
            "INSERT INTO UserDecks (google_id,json) VALUES  (%s, %s)", (google_id, json))
        user_deck_id = cursor.lastrowid
        cursor.connection.commit()
        cursor.close()
        return to_json(query_one("SELECT * FROM UserDecks WHERE deck_id = %s", user_deck_id))
    except:
        return '{"error":"not saved"}'


@app.route('/user/', methods=["PUT"])
def update_user_deck():
    try:
        json = request.args["json"]
        deck_id = request.args["deck_id"]
        cursor = get_cursor()
        cursor.execute(
            """UPDATE UserDecks SET json=%s WHERE deck_id=%s""", (json, deck_id))
        user_deck_id = cursor.lastrowid
        cursor.connection.commit()
        cursor.close()
        return to_json(query_one("SELECT * FROM UserDecks WHERE deck_id = %s", user_deck_id))
    except:
        return '{"error":"not saved"}'


@app.route('/user/<deck_id>', methods=["DELETE"])
def delete_user_deck(deck_id):
    try:
        cursor = get_cursor()
        cursor.execute(
            "DELETE FROM UserDecks WHERE deck_id=%s", (deck_id))
        cursor.connection.commit()
        cursor.close()
        return "{success:'OK'}"
    except:
        return '{"error":"deck not found"}'
