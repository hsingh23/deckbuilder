from app import app
import requests as r
from flask import request, session, g, redirect, url_for, abort, \
    render_template, flash, Response
from simplejson import dumps as to_json, loads as to_object
from quizlet import get_decks, parse_keywords
from util import combinations
from flask_oauth import OAuth
from __config import *

oauth = OAuth()
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={
                              'scope': 'https://www.googleapis.com/auth/userinfo.email',
                          'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={
                              'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)
REDIRECT_URI = '/oauth2callback'


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
    ret = to_json([item for sublist in combos for item in sublist])
    return Response(response=ret,
                    status=200,
                    mimetype="application/json")


@app.route('/login-with-google')
def login_with_google():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()

    return res.read()


@app.route('/login')
def login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {'Authorization': 'OAuth ' + access_token}
    user_information = to_object(r.get(url, headers=headers).text)
    from IPython import embed; embed()
    return redirect(url_for('index'))

@google.tokengetter
def get_access_token():
    return session.get('access_token')
