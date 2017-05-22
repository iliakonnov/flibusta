#!/usr/bin/python3.6
# -*- coding: utf8 -*-
import time
import datetime
import sqlite3
from itertools import islice, chain
from typing import List
from sys import argv


def initDb(conn: sqlite3.Connection):
    conn.executescript('''
    CREATE TABLE series (
        serie_id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    );

    CREATE TABLE books (
        book_id INTEGER PRIMARY KEY,
        title TEXT,
        serie_id INTEGER,
        serno INTEGER,
        size INTEGER,
        file TEXT,
        add_date DATE,
        lang TEXT,
        rate INTEGER,
        keywords TEXT,
        authors TEXT,
        genres TEXT,
        FOREIGN KEY(serie_id) REFERENCES series(serie_id)
    );

    CREATE TABLE authors (
        author_id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    );

    CREATE TABLE author_to_book (
        book_id INTEGER,
        author_id INTEGER,
        PRIMARY KEY(book_id, author_id),
        FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
        FOREIGN KEY(author_id) REFERENCES authors(author_id) ON DELETE CASCADE
    );

    CREATE TABLE genres (
        genre_id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    );

    CREATE TABLE genre_to_book (
        book_id INTEGER,
        genre_id INTEGER,
        PRIMARY KEY(book_id, genre_id),
        FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
        FOREIGN KEY(genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
    );

    CREATE TABLE series_temp (
        serie_id INTEGER,
        name TEXT
    );

    CREATE TABLE books_temp (
        book_id INTEGER,
        title TEXT,
        serie_id INTEGER,
        serno INTEGER,
        size INTEGER,
        file TEXT,
        add_date DATE,
        lang TEXT,
        rate INTEGER,
        keywords TEXT,
        authors TEXT,
        genres TEXT
    );

    CREATE TABLE authors_temp (
        author_id INTEGER,
        name TEXT
    );

    CREATE TABLE author_to_book_temp (
        book_id INTEGER,
        author_id INTEGER
    );

    CREATE TABLE genres_temp (
        genre_id INTEGER,
        name TEXT
    );

    CREATE TABLE genre_to_book_temp (
        book_id INTEGER,
        genre_id INTEGER
    );
    ''')
    conn.commit()


def doneDb(conn: sqlite3.Connection):
    print('Creating indexes and FTS...')
    conn.executescript('''
        CREATE INDEX idx_xxx_id ON books_temp(book_id);
        DELETE FROM books_temp
        WHERE rowid NOT IN(SELECT MAX(rowid)
                   FROM books_temp
                   GROUP BY book_id);

        CREATE INDEX idx_xx2_id ON genre_to_book_temp(book_id, genre_id);
        DELETE FROM genre_to_book_temp
        WHERE rowid NOT IN(SELECT MAX(rowid)
                   FROM genre_to_book_temp
                   GROUP BY book_id, genre_id);

        CREATE INDEX idx_xx3_id ON author_to_book_temp(book_id, author_id);
        DELETE FROM author_to_book_temp
        WHERE rowid NOT IN(SELECT MAX(rowid)
                   FROM author_to_book_temp
                   GROUP BY book_id, author_id);

        INSERT INTO series SELECT * FROM series_temp;
        INSERT INTO genres SELECT * FROM genres_temp;
        INSERT INTO authors SELECT * FROM authors_temp;
        INSERT INTO books SELECT * FROM books_temp;

        INSERT INTO genre_to_book SELECT * FROM genre_to_book_temp;
        INSERT INTO author_to_book SELECT * FROM author_to_book_temp;

        PRAGMA foreign_keys = ON;
        DELETE FROM authors WHERE name = '';
        DELETE FROM genres WHERE name = '';

        --CREATE INDEX books_id_idx ON books(book_id);

        --CREATE INDEX series_id_idx ON series(serie_id);
        --CREATE INDEX series_name_idx ON series(name);
        CREATE INDEX books_serie_idx ON books(serie_id);
        CREATE INDEX books_title_idx ON books(title);
        CREATE VIRTUAL TABLE series_fts USING fts4(name, tokenize=unicode61);
        INSERT INTO series_fts SELECT name FROM series;
        CREATE VIRTUAL TABLE titles_fts USING fts4(title, tokenize=unicode61);
        INSERT INTO titles_fts SELECT title FROM books;

        --CREATE INDEX authors_id_idx ON authors(author_id);
        --CREATE INDEX authors_name_idx ON authors(name);
        CREATE INDEX authorBook_book_idx ON author_to_book(book_id);
        CREATE INDEX authorBook_author_idx ON author_to_book(author_id);
        CREATE VIRTUAL TABLE authors_fts USING fts4(name, tokenize=unicode61);
        INSERT INTO authors_fts SELECT name FROM authors;

        --CREATE INDEX genres_id_idx ON genres(genre_id);
        --CREATE INDEX genres_name_idx ON genres(name);
        CREATE INDEX genreBook_book_idx ON genre_to_book(book_id);
        CREATE INDEX genreBook_author_idx ON genre_to_book(genre_id);

        DROP TABLE author_to_book_temp;
        DROP TABLE books_temp;
        DROP TABLE genre_to_book_temp;
        DROP TABLE genres_temp;
        DROP TABLE series_temp;
        DROP TABLE authors_temp;
    ''')
    conn.commit()
    print('Done!')


def addBooks(
    conn: sqlite3.Connection,
    books: List[dict],
    series: dict,
    genres: dict,
    authors: dict
):
    def chunks(iterable, size=10):
        # http://stackoverflow.com/a/24527424
        iterator = iter(iterable)
        for first in iterator:
            yield chain([first], islice(iterator, size - 1))

    chunkSize = 500

    print('Adding series...')
    serNum = 0
    serTotal = len(series)

    seriesIter = ((num, name) for name, num in series.items())
    for i in chunks(seriesIter, chunkSize):
        startTime = time.time()
        conn.executemany('INSERT INTO series_temp VALUES (?, ?)', i)
        conn.commit()
        endTime = time.time()

        serNum += chunkSize
        print('\t{n}/{t} ({s}) series added...'.format(
            n=serNum,
            t=serTotal,
            s=(endTime - startTime) / chunkSize
        ))
    print('Done.\n')

    print('Adding genres...')
    genreNum = 0
    genreTotal = len(genres)

    genresIter = ((num, name) for name, num in genres.items())
    for i in chunks(genresIter, chunkSize):
        startTime = time.time()
        conn.executemany('INSERT INTO genres_temp VALUES (?, ?)', i)
        conn.commit()
        endTime = time.time()
        genreNum += chunkSize
        print('\t{n}/{t} ({s}) genres added...'.format(
            n=genreNum,
            t=genreTotal,
            s=(endTime - startTime) / chunkSize
        ))
    print('Done.\n')

    print('Adding authors...')
    authorNum = 0
    authorTotal = len(authors)

    authorsIter = ((num, name) for name, num in authors.items())
    for i in chunks(authorsIter, chunkSize):
        startTime = time.time()
        conn.executemany('INSERT INTO authors_temp VALUES (?, ?)', i)
        conn.commit()
        endTime = time.time()
        authorNum += chunkSize
        print('\t{n}/{t} ({s}) authors added...'.format(
            n=authorNum,
            t=authorTotal,
            s=(endTime - startTime) / chunkSize
        ))
    print('Done.\n')

    print('Adding books...')
    bookNum = 0
    bookTotal = len(books)

    def booksIter():
        for i in books:
            yield {
                'book_id': i['lib_id'],
                'title': i['title'],
                'serie_id': series[i['series']],
                'serno': i['serno'],
                'size': i['size'],
                'file': i['file'],
                'add_date': int(time.mktime(
                    datetime.datetime.strptime(i['date'], "%Y-%m-%d").timetuple()
                )),
                'lang': i['lang'],
                'rate': i['librate'],
                'keywords': i['keywords'],
                'authors': i['author'],
                'genres': i['genre']
            }
    for i in chunks(booksIter(), chunkSize):
        startTime = time.time()
        conn.executemany('''
            INSERT INTO books_temp VALUES (
                :book_id,
                :title,
                :serie_id,
                :serno,
                :size,
                :file,
                :add_date,
                :lang,
                :rate,
                :keywords,
                :authors,
                :genres
            )
        ''', i)
        conn.commit()
        endTime = time.time()
        bookNum += chunkSize
        print('\t{n}/{t} ({s}) books added...'.format(
            n=bookNum,
            t=bookTotal,
            s=(endTime - startTime) / chunkSize
        ))
    print('Done.\n')

    print('Filling author2book...')
    a2bNum = 0

    def authorToBookIter():
        for b in books:
            for a in b['author'].split(':'):
                yield (b['lib_id'], authors[a])
    for i in chunks(authorToBookIter(), chunkSize):
        startTime = time.time()
        conn.executemany('INSERT INTO author_to_book_temp(book_id, author_id) VALUES (?, ?)', i)
        conn.commit()
        endTime = time.time()

        a2bNum += chunkSize
        print('\t{n} ({s}) added...'.format(n=a2bNum, s=(endTime - startTime) / chunkSize))
    print('Done.\n')

    print('Filling genre2book...')
    g2bNum = 0

    def genreToBookIter():
        for b in books:
            for g in b['genre'].split(':'):
                yield (b['lib_id'], genres[g])
    for i in chunks(genreToBookIter(), chunkSize):
        startTime = time.time()
        conn.executemany('INSERT INTO genre_to_book_temp(book_id, genre_id) VALUES (?, ?)', i)
        conn.commit()
        endTime = time.time()

        g2bNum += chunkSize
        print('\t{n} ({s}) added...'.format(n=g2bNum, s=(endTime - startTime) / chunkSize))
    print('Done.\n')

    print('Done all!')


def searchBooks(files):
    # .imp file format: github.com/rupor-github/InpxCreator/blob/master/lib2inpx/lib2inpx.cpp#L105
    # AUTHOR;GENRE;TITLE;SERIES;SERNO;FILE;SIZE;LIBID;DEL;EXT;DATE;LANG;LIBRATE;KEYWORDS;
    books = []
    series = {}
    genres = {}
    authors = {}

    serNum = 0
    genreNum = 0
    authorNum = 0
    n = 0

    for impFile in files:
        with open(impFile, 'r') as f:
            print('Parsing {}...'.format(impFile))
            for ln in f:
                splitted = ln.split('\x04')
                book = {
                    'author': splitted[0],
                    'genre': splitted[1],
                    'title': splitted[2],
                    'series': splitted[3],
                    'serno': int(splitted[4]) if splitted[4] else -1,
                    'file': impFile + '/' + splitted[5],
                    'size': int(splitted[6]),
                    'lib_id': splitted[7],
                    'del': splitted[8],
                    'ext': splitted[9],
                    'date': splitted[10],
                    'lang': splitted[11],
                    'librate': int(splitted[12]) if splitted[12] else -1,
                    'keywords': splitted[13]
                }

                series[book['series']] = serNum
                serNum += 1

                for g in book['genre'].split(':'):
                    genres[g] = genreNum
                    genreNum += 1

                for a in book['author'].split(':'):
                    authors[a] = authorNum
                    authorNum += 1

                books.append(book)
                n += 1

                if n % 800 == 0:
                    print('{} books found...'.format(n))

    print('{} books found!'.format(n))
    return {
        'books': books,
        'series': series,
        'genres': genres,
        'authors': authors
    }


if __name__ == "__main__":
    connection = sqlite3.connect('flibusta.sqlite')
    initDb(connection)
    data = searchBooks(argv[1:])
    addBooks(connection, **data)
    doneDb(connection)
