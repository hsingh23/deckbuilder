from app import app
from flask import request, session, g, redirect, url_for, abort, \
    render_template, flash
from forms import KeywordForm
from json import dumps as object_to_json, loads as json_to_object
from quizlet import get_decks


@app.route('/')
@app.route('/index')
def index():
    form = KeywordForm()
    if form.validate_on_submit():
        flash('Fetching your decks for ' + form.keywords.data)
    return render_template("index.html", form=form)


@app.route('/decks', methods=['GET', 'POST'])
def decks():
    form = KeywordForm(request.form)
    if form.validate():
        return get_decks(form.data["keywords"])
    return "Invalid form!"
