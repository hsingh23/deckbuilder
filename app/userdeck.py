import requests as r
# from config import *
from datetime import datetime, timedelta
from db import get_cursor, make_dicts, query_one, query_all
from app import app
from simplejson import dumps as to_json, loads as to_object, JSONDecodeError

def get_decks_from_database(user_id):
    cursor = get_cursor()
    output = cursor.execute("""
        SELECT json
        FROM UserDecks
        WHERE user_id = %s
    """, (user_id,))
    decks = make_dicts(cursor, cursor.fetchall())
    cursor.close()
    for deck in decks:
        try:
            deck["json"] = to_object(deck["json"])
        except JSONDecodeError:
            pass
    return decks

def save_to_db(all_sets_json, user_id):
  cursor = get_cursor()
  cursor.execute(
          "INSERT INTO UserDecks (user_id,json) VALUES  (%s, %s)", (user_id, json))
  cursor.connection.commit()
  cursor.close()

def _userdeck(all_sets_json, deck_id):
  cursor = get_cursor()
  cursor.execute(
      "UPDATE UserDecks SET json=%s WHERE deck_id=%s", (json,deck_id))
  cursor.connection.commit()
  cursor.close()

def delete_from_db(deck_id):
  cursor = get_cursor()
  cursor.execute(
          "DELETE FROM UserDecks WHERE deck_id=%s", (deck_id))
  cursor.connection.commit()
  cursor.close()
