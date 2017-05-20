#!/usr/bin/python3.6
# -*- coding: utf8 -*-
import base64
import sqlite3
from fb2reader import getBook
from time import time
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

    if not file_id:
        books = get_db().execute(
            'SELECT file FROM books WHERE book_id=?',
            (book_id,)
        ).fetchone()
        if books:
            file_id = books[0]
        else:
            return abort(400)

    book = getBook(file_id, ZIPPATH)
    if book['ok']:
        # ./inp/fb2-119691-132107.inp/120661
        book['result']['image'] = base64.b64encode(book['result']['image']).decode('utf-8') if isinstance(book['result']['image'], bytes) else book['result']['image']
        book['result']['book'] = base64.b64encode(book['result']['book']).decode('utf-8') if isinstance(book['result']['book'], bytes) else book['result']['book']
        return jsonify(book['result'])
    else:
        return abort(400)


@app.route('/search')
def search():
    startTime = time()

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

    params = {
        'limit': start + count if count else None,
        'lang': lang,
        'serno_max': serno_max,
        'serno_min': serno_min,
        'rate_max': rate_max,
        'rate_min': rate_min,
        'title': title,
        'serie': serie,
        'author': author,
        'genre': genre
    }

    parameters = {}
    for key, value in params.items():
        if value:
            parameters[key] = value

    result = get_db().execute('''
        WITH sel_books AS (
            SELECT {rowid} b.*, s.name AS serie
            FROM books b, series s
            WHERE b.serie_id = s.serie_id
                {lang}
                {serno_a} {serno_b}
                {rate_a} {rate_b}
                {title}
                {serie}
            ),
        sel_authors AS (
            SELECT a.name, b.book_id
            FROM authors a, author_to_book b
            WHERE a.author_id = b.author_id
                {author}
        ),
        sel_genres AS (
            SELECT g.name, b.book_id
            FROM genres g, genre_to_book b
            WHERE g.genre_id = b.genre_id
                {genre}
            )
        SELECT sel_books.*, sel_authors.name  author, sel_genres.name AS genre
        FROM sel_books, sel_authors, sel_genres
        WHERE sel_books.book_id = sel_authors.book_id
            AND sel_books.book_id = sel_genres.book_id
        {limit}
    '''.format(
        rowid='b.rowid, ' if count else '',
        limit='ORDER BY sel_books.rowid limit :limit' if count else '',
        lang='AND lang=:lang' if lang else '',
        serno_a='AND b.serno<=:serno_max' if serno_max else '',
        serno_b='AND b.serno>=:serno_min' if serno_min else '',
        rate_a='AND b.rate<=:rate_max' if rate_max else '',
        rate_b='AND b.rate>=:rate_min' if rate_min else '',
        title='''
            AND b.title IN (
                SELECT title FROM titles_fts WHERE title MATCH :title
            )''' if title else '',
        serie='''
            AND s.name IN (
                SELECT name FROM series_fts WHERE name MATCH :serie
            )''' if serie else '',
        author='''
            AND a.name IN (
               SELECT name
               FROM authors_fts
               WHERE name MATCH :author
            )''' if author else '',
        genre='AND name=":genre"' if genre else ''
    ), parameters)

    response = []
    if start:
        result.fetchmany(start)

    if count:
        for row in result.fetchmany(count):
            response.append(dict(zip(row.keys(), row)))
    else:
        for row in result:
            response.append(dict(zip(row.keys(), row)))

    return jsonify({
        'result': response,
        'parameters': parameters,
        'time': (time() - startTime) * 1000
    })


if __name__ == "__main__":
    from sys import argv
    ZIPPATH = argv[1]
    app.run(debug=True)
