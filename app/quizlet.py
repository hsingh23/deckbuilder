import requests as r
# from config import *
from datetime import datetime, timedelta
from db import get_cursor, get_dict_cursor
from app import app
QAPI_URL = "https://api.quizlet.com/2.0"
from simplejson import dumps as object_to_json, loads as json_to_object
QUIZLET_CLIENT_KEY = app.config["QUIZLET_CLIENT_KEY"]
cursor = get_cursor()
dict_cursor = get_dict_cursor()


def get_decks(keyword_string):
    res = {}
    for keyword in parse_keywords(keyword_string):
        keyword_id, last_updated, created = get_or_create_keyword(keyword)
        if expired_keyword(last_updated) or created:
            create_decks_from_quizlet(keyword, keyword_id)
        res[keyword] = get_decks_from_database(keyword)
    return object_to_json(res, use_decimal=True)


def expired_keyword(last_updated):
    return last_updated + timedelta(weeks=1) > datetime.now()


def get_or_create_keyword(keyword):
    created = False
    cursor.execute("""
        SELECT keyword_id, last_updated FROM Keywords where keyword = %s
    """, (keyword,))
    output = cursor.fetchone()
    if output:
        keyword_id, last_updated = output
    else:
        keyword_id = None
    if not keyword_id:
        created = True
        cursor.execute("""
            INSERT INTO Keywords (keyword) VALUES (%s)
        """, (keyword,))
        keyword_id = cursor.lastrowid
        last_updated = datetime.now()
    cursor.connection.commit()
    return keyword_id, last_updated, created


def get_decks_from_database(keyword):
    dict_cursor.execute("""
        SELECT keyword_id, keyword, json, terms_selected/GREATEST(times_deck_selected,1) as avg_selected
        FROM Keywords NATURAL JOIN KeywordsQuizletDecks NATURAL JOIN QuizletDecks
        WHERE keyword = %s
    """, (keyword,))
    return dict_cursor.fetchall()


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
        return (r.get(quizlet_sets_url).text)

    def save_to_db(all_sets_json, keyword_id):
        formated_json = [(x["id"], object_to_json(x))
                         for x in json_to_object(all_sets_json) if x["id"]]
        for quizlet_id, json in formated_json:
            cursor.callproc("create_or_update_quizlet", (quizlet_id, keyword_id, json))
            cursor.connection.commit()

    search_quizlet = QAPI_URL + \
        "/search/sets?client_id=%s&q=" % QUIZLET_CLIENT_KEY
    sets_info = json_to_object(
        r.get(search_quizlet + keyword + "&per_page=50&page=1").text)
    set_ids = parse_search(sets_info)
    all_sets_json = get_sets(set_ids)
    save_to_db(all_sets_json, keyword_id)
