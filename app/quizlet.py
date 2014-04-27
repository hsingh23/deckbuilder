import requests as r
# from config import *
from datetime import datetime, timedelta
from db import get_cursor, make_dicts, query_one, query_all
from app import app
QAPI_URL = "https://api.quizlet.com/2.0"
from simplejson import dumps as to_json, loads as to_object
QUIZLET_CLIENT_KEY = app.config["QUIZLET_CLIENT_KEY"]


def keyword_has_decks(keyword_id):
    res = query_one(
        "SELECT COUNT(*) FROM KeywordsQuizletDecks where keyword_id = %s", (keyword_id,))
    return res[0] > 1 if res else False


def get_decks(keyword_string):
    res = {}
    for keyword in parse_keywords(keyword_string):
        keyword_id, last_updated, created = get_or_create_keyword(keyword)
        if expired_keyword(last_updated) or created or not keyword_has_decks(keyword_id):
            create_decks_from_quizlet(keyword, keyword_id)
        res[keyword] = get_decks_from_database(keyword)
    return to_json(res, use_decimal=True)


def expired_keyword(last_updated):
    return last_updated + timedelta(weeks=1) < datetime.now()


def get_or_create_keyword(keyword):
    created = False
    output = query_one("""
        SELECT keyword_id, last_updated FROM Keywords where keyword = %s
    """, (keyword,))
    if output:
        keyword_id, last_updated = output
    else:
        keyword_id = None
    if not keyword_id:
        created = True
        cursor = get_cursor()
        cursor.execute("""
            INSERT INTO Keywords (keyword) VALUES (%s)
        """, (keyword,))
        keyword_id = cursor.lastrowid
        last_updated = datetime.now()
        cursor.connection.commit()
        cursor.close()
    return keyword_id, last_updated, created


def get_decks_from_database(keyword):
    cursor = get_cursor()
    output = cursor.execute("""
        SELECT keyword_id, keyword, json, terms_selected/GREATEST(times_deck_selected,1) as avg_selected
        FROM Keywords NATURAL JOIN KeywordsQuizletDecks NATURAL JOIN QuizletDecks
        WHERE keyword = %s
    """, (keyword,))
    decks = make_dicts(cursor, cursor.fetchall())
    cursor.close()
    for deck in decks:
        deck["json"] = to_object(deck["json"])
    return decks


def parse_keywords(keyword_string):
    if isinstance(keyword_string, unicode):
        keyword_string = keyword_string.encode('UTF-8')
    return map(lambda x: x.lower().strip(), keyword_string.split(","))


def create_decks_from_quizlet(keyword, keyword_id):
    def normalize(k):
        return k.encode('ascii', errors='backslashreplace') if isinstance(k, unicode) else k

    def parse_search(keyword_json):
        return [s["id"]for s in keyword_json["sets"]]

    def get_sets(set_ids):
        ids = ",".join(map(str, set_ids))
        quizlet_sets_url = "%s/sets?client_id=%s&set_ids=%s" % (
            QAPI_URL, QUIZLET_CLIENT_KEY, ids)
        all_sets_json = (r.get(quizlet_sets_url).text)
        return all_sets_json

    def save_to_db(all_sets_json, keyword_id):
        formated_json = [(x["id"], to_json(x))
                         for x in to_object(all_sets_json)]
        cursor = get_cursor()
        for quizlet_id, json in formated_json:
            cursor.callproc(
                "create_or_update_quizlet", (quizlet_id, keyword_id, json))
            cursor.connection.commit()
        cursor.close()
    search_quizlet = QAPI_URL + \
        "/search/sets?client_id=%s&q=" % QUIZLET_CLIENT_KEY
    sets_info = to_object(
        r.get(search_quizlet + keyword + "&per_page=50&page=1").text)
    set_ids = parse_search(sets_info)
    all_sets_json = get_sets(set_ids)
    save_to_db(all_sets_json, keyword_id)
