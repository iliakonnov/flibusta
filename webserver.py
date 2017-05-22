#!/usr/bin/python3.6
# -*- coding: utf8 -*-
import base64
import sqlite3
import api
from flask import Flask, request, jsonify, abort, g

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        conn = sqlite3.connect('flibusta.sqlite')
        conn.row_factory = sqlite3.Row

        db = g._database = conn
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/get')
def get():
    book_id = request.args.get('book_id', None)
    file_id = request.args.get('file', None)

    book = api.getBook(get_db(), ZIPPATH, book_id, file_id)
    if book['ok']:
        # ./inp/fb2-119691-132107.inp/120661
        book['result']['image'] = base64.b64encode(book['result']['image']).decode(
            'utf-8') if isinstance(book['result']['image'], bytes) else book['result']['image']
        book['result']['book'] = base64.b64encode(book['result']['book']).decode(
            'utf-8') if isinstance(book['result']['book'], bytes) else book['result']['book']
        return jsonify(book['result'])
    else:
        return abort(400, book['error'])


@app.route('/search')
def search():
    start = int(request.args.get('start', 0))
    count = int(request.args.get('count', 0))
    author = request.args.get('author', None)
    title = request.args.get('title', None)
    serie = request.args.get('serie', None)
    genre = request.args.get('genre', None)
    serno_min = request.args.get('serno_min', None)
    serno_max = request.args.get('seno_max', None)
    rate_min = request.args.get('rate_min', None)
    rate_max = request.args.get('rate_max', None)
    lang = request.args.get('lang', None)

    if (
        count < 1000 or
        [i for i in author if i.isalnum()] or
        [i for i in title if i.isalnum()] or
        [i for i in serie if i.isalnum()] or
        [i for i in genre if i.isalnum()]
    ):
        return jsonify(api.search(
            get_db(),
            start, count, author, title, serie, genre,
            serno_min, serno_max, rate_min, rate_max, lang
        ))
    else:
        return abort(400)


if __name__ == "__main__":
    from sys import argv
    ZIPPATH = argv[1]
    app.run(debug=True)
