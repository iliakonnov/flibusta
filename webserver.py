#!/usr/bin/python3.6
# -*- coding: utf8 -*-
import base64
import sqlite3
import api
from flask import Flask, request, jsonify, abort, render_template, g

app = Flask(__name__, static_url_path='/static/')


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


@app.route('/api/get')
def api_get():
    book_id = request.args.get('book_id', None)
    file_id = request.args.get('file', None)
    encoding = request.args.get('encoding', 'base64')

    book = api.getBook(get_db(), ZIPPATH, book_id, file_id)

    if encoding == 'base64':
        encoder = base64.b64encode
    elif encoding == 'ascii85':
        encoder = base64.a85encode
    else:
        return abort(400, 'Unknown encoding')

    if book['ok']:
        if isinstance(book['result']['image'], bytes):
            book['result']['image'] = encoder(book['result']['image']).decode('utf-8')
        if isinstance(book['result']['book'], bytes):
            book['result']['book'] = encoder(book['result']['book']).decode('utf-8')
        return jsonify(book['result'])
    else:
        return abort(400, book['error'])


@app.route('/api/search')
def api_search():
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
        (count < 1000 and count > 0) or
        [i for i in author if i.isalnum()] or
        [i for i in title if i.isalnum()] or
        [i for i in serie if i.isalnum()]
    ):
        return jsonify(api.search(
            get_db(),
            start, count, author, title, serie, genre,
            serno_min, serno_max, rate_min, rate_max, lang
        ))
    else:
        return abort(400)


@app.route('/book/<book_id>')
def bookInfo(book_id):
    pass


@app.route('/search')
def search():
    pass


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/css.css')
def css():
    return app.send_static_file('css.css')


if __name__ == "__main__":
    from sys import argv
    import os
    ZIPPATH = argv[1]
    app.run(debug=True)
