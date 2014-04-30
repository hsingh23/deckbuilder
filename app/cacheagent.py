import requests as r
import redis
# from config import *
from datetime import datetime, timedelta
from db import get_cursor, make_dicts, query_one, query_all

def get_most_searched_decks():
  return query_all("""SELECT keyword_id, keyword, json, terms_selected/GREATEST(times_deck_selected,1) as avg_selected
        FROM Keywords NATURAL JOIN KeywordsQuizletDecks NATURAL JOIN QuizletDecks
        Order By times_searched DESC LIMIT 1000;""")
