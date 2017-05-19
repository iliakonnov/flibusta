#!/usr/bin/python3.6
# -*- coding: utf8 -*-
import sqlite3
from flask import Flask, request, jsonify, g

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('flibusta.sqlite')
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/all')
def getAll():
    result = []
    for i in get_db().execute('SELECT * FROM books LIMIT 1000'):
        result.append(tuple(i))
    return jsonify(result)


@app.route('/search')
def search():
    start = request.args.get('start', 0)
    count = request.args.get('count', None)
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

    def check(sql):
        print(sql)
        return sql

    result = get_db().execute(check('''
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
        serno_a='AND b.serno<:serno_max' if serno_max else '',
        serno_b='AND b.serno>:serno_min' if serno_min else '',
        rate_a='AND b.rate<:rate_max' if rate_max else '',
        rate_b='AND b.rate>:rate_min' if rate_min else '',
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
    )), parameters)

    response = []
    if count:
        result.fetchmany(count)
        row = result.fetchone()
        while row:
            response.append(dict(zip(row.keys(), row)))
    return jsonify({
        'result': response,
        'parameters': parameters
    })


if __name__ == "__main__":
    app.run(debug=True)
