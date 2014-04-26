import requests as r
# from config import *
from db import get_connection
from app import app
QAPI_URL = "https://api.quizlet.com/2.0"
from json import dumps as object_to_json, loads as json_to_object
QUIZLET_CLIENT_KEY = app.config["QUIZLET_CLIENT_KEY"]


def to_json(obj):
    return object_to_json(obj)


def get_keyword_from_database(keyword):
    c = get_connection().cursor()
    c.execute("""
        SELECT json
        FROM Keywords NATURAL JOIN KeywordsQuizletDecks NATURAL JOIN QuizletDecks
        WHERE keyword = %s
    """, (keyword,))
    res = c.fetchall()
    return res


def get_keyword_from_quizlet(keyword):
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

    def format_all_sets(all_sets_json):
        return [(x["id"], object_to_json(x)) for x in json_to_object(sets_term)]

    search_quizlet = QAPI_URL + \
        "/search/sets?client_id=%s&q=" % QUIZLET_CLIENT_KEY
    sets_info = json_to_object(
        r.get(search_quizlet + keyword + "&per_page=50&page=1").text)
    set_ids = parse_search(sets_info)
    all_sets_json = get_sets(set_ids)
    return format_all_sets(all_sets_json)


def parse_keywords(keyword_string):
    if isinstance(keyword_string, unicode):
        keyword_string = keyword_string.encode('UTF-8')
    return map(lambda x: x.lower().strip(), keyword_string.split(","))


def get_decks(keyword_string):
    res = []
    for keyword in parse_keywords(keyword_string):
        results = get_keyword_from_database(keyword)
        if not results:
            results = get_keyword_from_quizlet(keyword)
    return to_json(results)
