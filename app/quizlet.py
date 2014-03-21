import requests as r
# from config import *
from db import get_cursor
from app import app
QAPI_URL = "https://api.quizlet.com/2.0"
from json import dumps as object_to_json, loads as json_to_object
QUIZLET_CLIENT_KEY = app.config["QUIZLET_CLIENT_KEY"]


def to_json(obj):
    return object_to_json(obj)


def get_keyword_from_database(keyword):
    c = get_cursor()
    c.execute("""
        SELECT title, qid, front, back, position, qhas_images
        FROM Keyword
        NATURAL JOIN KeywordDeck
        NATURAL JOIN Deck
        NATURAL JOIN CardDeck
        NATURAL JOIN Card
        WHERE text = %s
        GROUP BY did;
    """, (keyword,))
    res = c.fetchall()
    return res


def normalize(k):
    return k.encode('ascii', errors='backslashreplace') if isinstance(k, unicode) else k


def get_keyword_from_quizlet(keyword):
    def parse_search(keyword_json):
        return [s["id"]for s in keyword_json["sets"]]

    def get_sets(set_ids):
        ids = ",".join(map(str, set_ids))
        quizlet_sets_url = "%s/sets?client_id=%s&set_ids=%s" % (
            QAPI_URL, QUIZLET_CLIENT_KEY, ids)
        return json_to_object(r.get(quizlet_sets_url).text)

    def merge(sets_terms, set_ids, keyword):
        c = get_cursor()
        decks = [map(normalize, (i["id"], i["url"], i["title"], i["created_by"], i["term_count"], i["created_date"], i["modified_date"], i[
                     "has_images"], i["subjects"], i["description"], i["lang_terms"], i["lang_definitions"], i["has_discussion"])) for i in sets_terms]
        try:
            c.executemany("""
                    INSERT INTO Deck (qid, url, title, qcreated_by, qterm_count, qcreated_date, 
                        qmodified_date, qhas_images, qsubject, qdescription, qlang_term, qlang_definitions, qhas_discussion)
                    VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")""", decks )
        except:
            pass
        # for i in sets_terms:
        #     c.execute(""" INSERT INTO Card (front, back)
        #         """, i[term_count])
        #     qid

    search_quizlet = QAPI_URL + \
        "/search/sets?client_id=%s&q=" % QUIZLET_CLIENT_KEY
    # with_images = json_to_object(r.get(search_quizlet+keyword+"&images_only=true&sort=most_studied").text)
    sets_info = json_to_object(
        r.get(search_quizlet + keyword + "&sort=most_studied&per_page=50&page=1").text)
    set_ids = parse_search(sets_info)
    sets_term = get_sets(set_ids)
    merge(sets_term, set_ids, keyword)
    results = merge(sets_term, set_ids, keyword)
    return sets_term
    # return get_keyword_from_database(keyword)


def parse_keywords(keyword_string):
    if isinstance(keyword_string, unicode):
        keyword_string = keyword_string.encode('UTF-8')
    return map(str.strip, keyword_string.split(","))


def get_decks(keyword_string):
    res = []
    for keyword in parse_keywords(keyword_string):
        results = get_keyword_from_database(keyword)
        if not results:
            results = get_keyword_from_quizlet(keyword)
    return to_json(results)
