from app import app
from flask import request, session, g, redirect, url_for, abort, \
    render_template, flash, Response
from json import dumps as object_to_json, loads as json_to_object
from quizlet_backup import get_decks, parse_keywords
from util import combinations


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/decks/<keywords>')
def decks(keywords):
    ret = get_decks(keywords)
    return Response(response=ret,
                    status=200,
                    mimetype="application/json")


@app.route('/combinations', methods=["GET", "POST"])
def keyword_combinations():
    keywords = parse_keywords(request.args["k"])
    combos = [list(combinations(keywords, i))
              for i in xrange(len(keywords), 1, -1)]
    ret = object_to_json([item for sublist in combos for item in sublist])
    return Response(response=ret,
                    status=200,
                    mimetype="application/json")
