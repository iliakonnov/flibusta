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

    CREATE TABLE serie_to_book (
        book_id INTEGER,
        serie_id INTEGER,
        serno INTEGER,
        PRIMARY KEY(book_id, serie_id),
        FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
        FOREIGN KEY(serie_id) REFERENCES series(serie_id) ON DELETE CASCADE
    );

    CREATE TABLE books (
        book_id INTEGER PRIMARY KEY,
        title TEXT,
        title_alt TEXT,
        size INTEGER,
        file TEXT,
        add_date DATE,
        lang TEXT,
        rate INTEGER,
        keywords TEXT,
        deleted INTEGER,
        joined_into INTEGER,
        
        authors TEXT,
        series TEXT,
        genres TEXT,

        FOREIGN KEY(joined_into) REFERENCES books(book_id)
    );

    CREATE TABLE authors (
        author_id INTEGER PRIMARY KEY,
        first_name TEXT,
        middle_name TEXT,
        last_name TEXT,
        nickname TEXT,
        name TEXT
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
    
    CREATE TABLE keywords (
        keyword_id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    );

    CREATE TABLE keyword_to_book (
        book_id INTEGER,
        keyword_id INTEGER,
        PRIMARY KEY(book_id, keyword_id),
        FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
        FOREIGN KEY(keyword_id) REFERENCES keywords(keyword_id) ON DELETE CASCADE
    );

    CREATE TABLE series_temp (
        serie_id INTEGER,
        name TEXT
    );

    CREATE TABLE serie_to_book_temp (
        book_id INTEGER,
        serie_id INTEGER,
        serno INTEGER
    );

    CREATE TABLE books_temp (
        book_id INTEGER,
        title TEXT,
        title_alt TEXT,
        size INTEGER,
        file TEXT,
        add_date DATE,
        lang TEXT,
        rate INTEGER,
        deleted INTEGER,
        joined_into INTEGER
    );

    CREATE TABLE authors_temp (
        author_id INTEGER,
        first_name TEXT,
        middle_name TEXT,
        last_name TEXT,
        nickname TEXT
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
    
    CREATE TABLE keywords_temp (
        keyword_id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    );

    CREATE TABLE keyword_to_book_temp (
        book_id INTEGER,
        keyword_id INTEGER
    );
    ''')
    conn.commit()


def doneDb(conn: sqlite3.Connection):
    print('Creating indexes and FTS...')
    sql = '''
        -- Removing duplicates
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

        CREATE INDEX idx_xx4_id ON serie_to_book_temp(book_id, serie_id);
        DELETE FROM serie_to_book_temp
        WHERE rowid NOT IN(SELECT MAX(rowid)
                   FROM serie_to_book_temp
                   GROUP BY book_id, serie_id);

        CREATE INDEX idx_xx5_id ON keyword_to_book_temp(book_id, keyword_id);
        DELETE FROM keyword_to_book_temp
        WHERE rowid NOT IN(SELECT MAX(rowid)
                   FROM keyword_to_book_temp
                   GROUP BY book_id, keyword_id);

        INSERT INTO series SELECT * FROM series_temp;
        INSERT INTO genres SELECT * FROM genres_temp;
        INSERT INTO authors
        SELECT
            a.*,
            (a.first_name || ' ' || a.middle_name || ' ' || a.last_name || ' ' || a.nickname) as name 
        FROM authors_temp a;
        INSERT INTO keywords SELECT * FROM keywords_temp;

        INSERT INTO genre_to_book SELECT * FROM genre_to_book_temp;
        INSERT INTO author_to_book SELECT * FROM author_to_book_temp;
        INSERT INTO serie_to_book SELECT * FROM serie_to_book_temp;
        INSERT INTO keyword_to_book SELECT * FROM keyword_to_book_temp;

        PRAGMA foreign_keys = ON;
        DELETE FROM authors WHERE name = '' OR name = '   ';
        DELETE FROM genres WHERE name = '';
        DELETE FROM series WHERE name = '';
        DELETE FROM keywords WHERE name = '';

        CREATE INDEX serieBook_book_idx ON serie_to_book(book_id);
        CREATE INDEX serieBook_serie_idx ON serie_to_book(serie_id);
        CREATE VIRTUAL TABLE series_fts USING fts4(name, tokenize=unicode61);
        INSERT INTO series_fts SELECT name FROM series;

        CREATE INDEX authorBook_book_idx ON author_to_book(book_id);
        CREATE INDEX authorBook_author_idx ON author_to_book(author_id);
        CREATE VIRTUAL TABLE authors_fts USING fts4(name, tokenize=unicode61);
        INSERT INTO authors_fts SELECT name FROM authors;

        CREATE INDEX genreBook_book_idx ON genre_to_book(book_id);
        CREATE INDEX genreBook_genre_idx ON genre_to_book(genre_id);
        
        CREATE INDEX keywordBook_book_idx ON keyword_to_book(book_id);
        CREATE INDEX keywordBook_keyword_idx ON keyword_to_book(keyword_id);
        CREATE VIRTUAL TABLE keywords_fts USING fts4(name, tokenize=unicode61);
        INSERT INTO keywords_fts SELECT name FROM keywords;
        
        INSERT INTO books
        SELECT b.*,
            NULL as authors,
            NULL as series,
            NULL AS genres,
            NULL as keywords
        FROM books_temp b;

        UPDATE books
        SET authors = (
            SELECT group_concat(a.author_id || '###' || a.name, '$$$')
            FROM authors a,
                 author_to_book ab
            WHERE a.author_id = ab.author_id
              AND books.book_id = ab.book_id
        );

        UPDATE books
        SET series = (
            SELECT group_concat(s.serie_id || '###' || s.name || '###' || sb.serno, '$$$')
            FROM series s,
                 serie_to_book sb
            WHERE s.serie_id = sb.serie_id
              AND books.book_id = sb.book_id
        );
        
        UPDATE books
        SET genres = (
            SELECT group_concat(g.genre_id || '###' || g.name, '$$$')
            FROM genres g,
                 genre_to_book gb
            WHERE g.genre_id = gb.genre_id
              AND books.book_id = gb.book_id
        );
           
        UPDATE books
        SET keywords = (
               SELECT group_concat(kw.keyword_id || '###' || kw.name, '$$$')
               FROM keywords kw,
                    keyword_to_book kwb
               WHERE kw.keyword_id = kwb.keyword_id
                 AND books.book_id = kwb.book_id
           );
        
        CREATE INDEX books_title_idx ON books(title);
        CREATE INDEX books_title_alt_idx ON books(title_alt);
        CREATE VIRTUAL TABLE titles_fts USING fts4(title, tokenize=unicode61);
        INSERT INTO titles_fts SELECT title FROM books;
        CREATE VIRTUAL TABLE titles_alt_fts USING fts4(title, tokenize=unicode61);
        INSERT INTO titles_alt_fts SELECT title_alt FROM books;

        --DROP TABLE author_to_book_temp;
        --DROP TABLE books_temp;
        --DROP TABLE genre_to_book_temp;
        --DROP TABLE genres_temp;
        --DROP TABLE series_temp;
        --DROP TABLE authors_temp;
        --DROP TABLE serie_to_book_temp;
        --DROP TABLE keywords_temp;
        --DROP TABLE keyword_to_book_temp;
        
        --VACUUM;
    '''
    # conn.executescript(sql)
    for part in sql.split(';'):
        print(part)
        conn.executescript(part + ';')
    conn.commit()
    print('Done!')


def addBooks(
    conn: sqlite3.Connection,
    books: List[dict],
    series: dict,
    genres: dict,
    authors: dict,
    keywords: dict
):
    def chunks(iterable, size=10):
        # http://stackoverflow.com/a/24527424
        iterator = iter(iterable)
        for first in iterator:
            yield chain([first], islice(iterator, size - 1))

    chunkSize = 250000

    print('Adding series...')
    serNum = 0
    serTotal = len(series)

    seriesIter = ((num['serie_id'], name) for name, num in series.items())
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

    authorsIter = ((num, *name) for name, num in authors.items())
    for i in chunks(authorsIter, chunkSize):
        startTime = time.time()
        conn.executemany('INSERT INTO authors_temp(author_id, first_name, middle_name, last_name, nickname) VALUES (?, ?, ?, ?, ?)', i)
        conn.commit()
        endTime = time.time()
        authorNum += chunkSize
        print('\t{n}/{t} ({s}) authors added...'.format(
            n=authorNum,
            t=authorTotal,
            s=(endTime - startTime) / chunkSize
        ))
    print('Done.\n')

    print('Adding keywords...')
    keywordsNum = 0
    keywordsTotal = len(keywords)

    keywordsIter = ((num, name) for name, num in keywords.items())
    for i in chunks(keywordsIter, chunkSize):
        startTime = time.time()
        conn.executemany('INSERT INTO keywords_temp VALUES (?, ?)', i)
        conn.commit()
        endTime = time.time()
        keywordsNum += chunkSize
        print('\t{n}/{t} ({s}) keywords added...'.format(
            n=keywordsNum,
            t=keywordsTotal,
            s=(endTime - startTime) / chunkSize
        ))
    print('Done.\n')

    print('Adding books...')
    bookNum = 0
    bookTotal = len(books)

    for i in chunks(books, chunkSize):
        startTime = time.time()
        conn.executemany('''
            INSERT INTO books_temp VALUES (
                :book_id,
                :title,
                :title_alt,
                :size,
                :file,
                :add_date,
                :lang,
                :rate,
                :deleted,
                :joined_into
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
            for a in b['authors']:
                yield (b['book_id'], authors[a])
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
            for g in b['genres']:
                yield (b['book_id'], genres[g])
    for i in chunks(genreToBookIter(), chunkSize):
        startTime = time.time()
        conn.executemany('INSERT INTO genre_to_book_temp(book_id, genre_id) VALUES (?, ?)', i)
        conn.commit()
        endTime = time.time()

        g2bNum += chunkSize
        print('\t{n} ({s}) added...'.format(n=g2bNum, s=(endTime - startTime) / chunkSize))
    print('Done.\n')

    print('Filling serie2book')
    s2bnum = 0

    def serieToBookIter():
        for b in books:
            for sername, serno in b['series'].items():
                s = series[sername]
                if s['zero'] and serno is not None and serno != -1:
                    serno += 1
                yield (b['book_id'], s['serie_id'], serno)
    for i in chunks(serieToBookIter(), chunkSize):
        startTime = time.time()
        conn.executemany('INSERT INTO serie_to_book_temp(book_id, serie_id, serno) VALUES (?, ?, ?)', i)
        conn.commit()
        endTime = time.time()

        s2bnum += chunkSize
        print('\t{n} ({s}) added...'.format(n=s2bnum, s=(endTime - startTime) / chunkSize))

    print('Filling keyword2book...')
    kw2bNum = 0

    def keywordToBookIter():
        for b in books:
            for kw in b['keywords']:
                yield (b['book_id'], keywords[kw])
    for i in chunks(keywordToBookIter(), chunkSize):
        startTime = time.time()
        conn.executemany('INSERT INTO keyword_to_book_temp(book_id, keyword_id) VALUES (?, ?)', i)
        conn.commit()
        endTime = time.time()

        kw2bNum += chunkSize
        print('\t{n} ({s}) added...'.format(n=kw2bNum, s=(endTime - startTime) / chunkSize))
    print('Done.\n')

    print('Done all!')


def searchBooks(files):
    # .imp file format: github.com/rupor-github/InpxCreator/blob/master/lib2inpx/lib2inpx.cpp#L105
    # AUTHOR;GENRE;TITLE;SERIES;SERNO;FILE;SIZE;LIBID;DEL;EXT;DATE;LANG;LIBRATE;KEYWORDS;
    books = []
    series = {}
    genres = {}
    authors = {}
    keywords = {}

    n = 0

    for impFile in files:
        with open(impFile, 'r') as f:
            print('Parsing {}...'.format(impFile))
            for ln in f:
                splitted = ln.split('\x04')
                book = {
                    'authors': splitted[0].split(':'),
                    'genres': splitted[1].split(':'),
                    'title': splitted[2],
                    'title_alt': None,
                    'series': {},
                    'file': impFile + '/' + splitted[5],
                    'size': int(splitted[6]),
                    'book_id': splitted[7],
                    'deleted': splitted[8],
                    'ext': splitted[9],
                    'add_date': splitted[10],
                    'lang': splitted[11],
                    'rate': int(splitted[12]) if splitted[12] else -1,
                    'keywords': [i.strip() for i in splitted[13].split(',')],
                    'joined_into': None
                }

                book['add_date'] = int(time.mktime(
                    datetime.datetime.strptime(book['add_date'], "%Y-%m-%d").timetuple()
                ))

                if splitted[3] or splitted[4]:
                    sername = splitted[3]
                    serno = splitted[4]
                    if serno:
                        if serno.isnumeric():
                            serno = int(serno)
                        else:
                            serno = -1
                    else:
                        serno = None
                    book['series'][sername] = serno
                    if sername not in series:
                        series[sername] = {
                            'serie_id': len(series),
                            'zero': serno == 0
                        }
                    elif serno == 0:
                        series[sername]['zero'] = True

                for g in book['genres']:
                    if g not in genres:
                        genres[g] = len(genres)

                new_authors = []
                for a in book['authors']:
                    if not a:
                        a = ('', '', '', '')
                    else:
                        splitted = a.rsplit(',', 2)
                        if len(splitted) == 3:
                            a = (*splitted, '')
                        elif len(splitted) == 2:
                            a = (*splitted, '', '')
                        elif len(splitted) == 1:
                            a = (*splitted, '', '', '')
                        else:
                            raise Exception('Unreachable')
                    if a not in authors:
                        authors[a] = len(authors)
                    new_authors.append(a)
                book['authors'] = new_authors

                for kw in book['keywords']:
                    if kw not in keywords:
                        keywords[kw] = len(keywords)

                books.append(book)
                n += 1

                if n % 800 == 0:
                    print('{} books found...'.format(n))

    print('{} books found!'.format(n))
    return {
        'books': books,
        'series': series,
        'genres': genres,
        'authors': authors,
        'keywords': keywords,
    }


def load_mysql(*args, **kwargs):
    import pymysql
    con = pymysql.connect(*args, **kwargs)
    with con.cursor() as cur:
        pass


if __name__ == "__main__":
    connection = sqlite3.connect('flibusta.sqlite')
    initDb(connection)
    data = searchBooks(argv[1:])
    addBooks(connection, **data)
    doneDb(connection)
