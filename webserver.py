#!/usr/bin/python3.6
# -*- coding: utf8 -*-
import base64
import sqlite3
import api
import time
from flask import Flask, request, jsonify, abort, render_template, g

app = Flask(__name__, static_url_path='/static/')

PARAMS_TRANSLATION = {
    'author': 'Автор',
    'title': 'Название',
    'serie': 'Серия',
    'genre': 'Жанр',
    'serno_min': 'Минимальный номер в серии',
    'serno_max': 'Максимальный номер в серии',
    'rate_min': 'Минимальный рейтинг книги',
    'rate_max': 'Максимальный рейтинг книги',
    'lang': 'Язык'
}


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


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: (time.time() - g.request_start_time) * 1000


@app.route('/api/get')
def api_get():
    book_id = request.args.get('book_id', None)
    encoding = request.args.get('encoding', 'base64')

    book = api.getBook(get_db(), ZIPPATH, book_id)

    if encoding == 'base64':
        encoder = base64.b64encode
    elif encoding == 'ascii85':
        encoder = base64.a85encode
    else:
        return abort(400, 'Unknown encoding')

    if book['ok']:
        if isinstance(book['fb2']['image'], bytes):
            book['fb2']['image'] = encoder(book['fb2']['image']).decode('utf-8')
        if isinstance(book['fb2']['book'], bytes):
            book['fb2']['book'] = encoder(book['fb2']['book']).decode('utf-8')
        return jsonify({
            'db': book['db'],
            'fb2': book['fb2']
        })
    else:
        return abort(400, book['error'])


@app.route('/api/search')
def api_search():
    book_id = request.args.get('book_id', None)
    author_id = request.args.get('author_id', None)
    serie_id = request.args.get('serie_id', None)
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
        book_id or author_id or serie_id or
        (count < 1000 and count > 0) or
        (author and [i for i in author if i.isalnum()]) or
        (title and [i for i in title if i.isalnum()]) or
        (serie and [i for i in serie if i.isalnum()])
    ):
        return jsonify(api.search(
            get_db(),
            book_id, author_id, serie_id,
            start, count, author, title, serie, genre,
            serno_min, serno_max, rate_min, rate_max, lang
        ))
    else:
        return abort(400)


@app.route('/serie/<serie_id>')
def serieInfo(serie_id):
    books = api.search(get_db(), serie_id=serie_id)
    return render_template('list.html', books=books['result'], listName='Серия')


@app.route('/book/<book_id>')
def bookInfo(book_id):
    book = api.getBook(get_db(), ZIPPATH, book_id)
    if book['ok']:
        if isinstance(book['fb2']['image'], bytes):
            book['fb2']['image'] = base64.b64encode(book['fb2']['image']).decode('utf-8')
        if isinstance(book['fb2']['book'], bytes):
            book['fb2']['book'] = base64.b64encode(book['fb2']['book']).decode('utf-8')
        result = {
            'db': book['db'],
            'fb2': book['fb2']
        }
        return render_template('book.html', book=result)
    else:
        return render_template('searchError.html')


@app.route('/search')
def search():
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
        (author and [i for i in author if i.isalnum()]) or
        (title and [i for i in title if i.isalnum()]) or
        (serie and [i for i in serie if i.isalnum()])
    ):
        result = api.search(
            get_db(),
            None, None, None,
            0, 0, author, title, serie, genre,
            serno_min, serno_max, rate_min, rate_max, lang
        )
        return render_template(
            'search.html',
            params_translation=PARAMS_TRANSLATION,
            result=result
        )
    else:
        return render_template('searchError.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/css.css')
def css():
    return app.send_static_file('css.css')


@app.route('/index.js')
def indexJs():
    return app.send_static_file('index.js')


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


if __name__ == "__main__":
    from sys import argv
    ZIPPATH = argv[1]
    app.run(host='0.0.0.0', debug=True)
