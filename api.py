from time import time
from fb2reader import getBook as getFb2


def getBook(conn, zippath, book_id=None):
    book = search(conn, book_id=book_id)
    if book['ok']:
        if book['result']:
            book = book['result'][0]
            file_id = book['file']
        else:
            return {
                'ok': False,
                'error': 'Book not found'
            }
    else:
        return book

    fb2 = getFb2(file_id, zippath)

    if fb2['ok']:
        return {
            'ok': True,
            'fb2': fb2['result'],
            'db': book
        }
    else:
        return fb2


def getAuthors(conn, book_id):
    result = conn.execute('''
        SELECT author_id, name FROM authors WHERE author_id IN (
            SELECT author_id FROM author_to_book WHERE book_id=?
        );
    ''', (book_id, ))
    if result:
        return {
            'ok': True,
            'result': [dict(zip(row.keys(), row)) for row in result]
        }
    else:
        return {
            'ok': False,
            'error': 'Book or author not found'
        }


def getAuthorName(conn, author_id):
    result = conn.execute('SELECT name FROM authors WHERE author_id=?', (author_id, )).fetchone()
    if result:
        return {
            'ok': True,
            'result': result[0]
        }
    else:
        return {
            'ok': False,
            'error': 'Author not found'
        }


def getSerieName(conn, serie_id):
    result = conn.execute('SELECT name FROM series WHERE serie_id=?', (serie_id, )).fetchone()
    if result:
        return {
            'ok': True,
            'result': result[0]
        }
    else:
        return {
            'ok': False,
            'error': 'Serie not found'
        }


def split_ids(joined, mapper):
    if not joined:
        return []
    result = []
    for i in joined.split('$$$'):
        splitted = i.split('###')
        if len(splitted) != len(mapper):
            raise Exception('Invalid pair={!r} with mapper={!r}'.format(i, mapper))
        result.append(dict((
            (i[1], i[0](splitted[n])) for n, i in enumerate(mapper)
        )))
    return result


def search(
        conn,
        book_id=None, author_id=None, serie_id=None, genre_id=None, keyword_id=None, order=None,
        start=0, count=0, author=None, title=None, serie=None, genre=None, keyword=None,
        rate_min=None, rate_max=None, lang=None
):
    startTime = time()

    order_new = 'ORDER BY b.deleted ASC'
    if not order and (count or start):
        order_new += ', b.book_id'
    elif not order:
        order_new += ''
    elif order in ['book_id', 'rate', 'size', 'title']:
        order_new += ', b.' + order
    elif order == 'serno':
        if serie_id is None:
            return {'ok': False, 'error': 'serie_id not specified. Unable to order by serno'}
        order_new += ''', (
             SELECT serno
             FROM serie_to_book sb
             WHERE sb.serie_id = :serie_id
               AND sb.book_id = b.book_id
        )
        '''
    else:
        return {'ok': False, 'error': 'Unknown order'}

    params = {
        'count': start + count if count else None,
        'book_id': book_id,
        'author_id': author_id,
        'serie_id': serie_id,
        'genre_id': genre_id,
        'keyword_id': keyword_id,
        'lang': lang,
        'rate_max': rate_max,
        'rate_min': rate_min,
        'title': title,
        'serie': serie,
        'author': author,
        'order': order,
        'genre': genre,
        'keyword': keyword,
    }
    order = order_new

    parameters = {}
    for key, value in params.items():
        if value:
            parameters[key] = value

    sql = '''
        SELECT b.*
        FROM books b
        WHERE 1
        {book_id}
        {author_id}
        {serie_id}
        {genre_id}
        {keyword_id}

        {lang}
        {rate_a} {rate_b}
        {title}
        {serie}
        {author}
        {genre}
        {keyword}
        {order}
        {limit}
    '''.format(
        book_id='AND b.book_id=:book_id' if book_id else '',
        author_id='''
            AND b.book_id IN (
                SELECT book_id FROM author_to_book WHERE author_id=:author_id
            )''' if author_id else '',
        serie_id='''
            AND b.book_id IN (
                SELECT s.book_id
                FROM serie_to_book s
                WHERE s.serie_id = :serie_id
            )
        ''' if serie_id else '',
        genre_id='''
            AND b.book_id IN (
                SELECT g.book_id
                FROM genre_to_book g
                WHERE g.genre_id = :genre_id
            )
        ''' if genre_id else '',
        keyword_id='''
            AND b.book_id IN (
                SELECT kw.book_id
                FROM keyword_to_book kw
                WHERE kw.keyword_id = :keyword_id
            )
        ''' if keyword_id else '',
        lang='AND b.lang=:lang' if lang else '',
        rate_a='AND b.rate<=:rate_max' if rate_max else '',
        rate_b='AND b.rate>=:rate_min' if rate_min else '',
        title='''
            AND b.title IN (
                SELECT title FROM titles_fts WHERE title MATCH :title
            )''' if title else '',
        serie='''
            AND b.book_id IN (
                SELECT b.book_id
                FROM series s, serie_to_book b
                WHERE s.serie_id = b.serie_id
                    AND s.name IN (
                        SELECT name
                        FROM series_fts
                        WHERE name MATCH :serie
                    )
            )''' if serie else '',
        author='''
            AND b.book_id IN (
                SELECT b.book_id
                FROM authors a, author_to_book b
                WHERE a.author_id = b.author_id
                    AND a.name IN (
                       SELECT name
                       FROM authors_fts
                       WHERE name MATCH :author
                    )
            )''' if author else '',
        genre='''
            AND b.book_id IN (
                SELECT b.book_id
                FROM genres g, genre_to_book b
                WHERE g.genre_id = b.genre_id
                    AND g.name=:genre
            )''' if genre else '',
        keyword='''
            AND b.book_id IN (
                SELECT b.book_id
                FROM keywords kw, keyword_to_book b
                WHERE kw.keyword_id = b.keyword_id
                    AND kw.name=:keyword
            )''' if keyword else '',
        order=order,
        limit='LIMIT :count' if count else ''
    )
    sqlTime = time()
    result = conn.execute(sql, parameters)
    sqlEnd = time()

    response = []
    if start:
        result.fetchmany(start)

    if count:
        for row in result.fetchmany(count):
            response.append(dict(zip(row.keys(), row)))
    else:
        for row in result:
            response.append(dict(zip(row.keys(), row)))
    for i in response:
        i['authors'] = split_ids(i['authors'], ((int, 'id'), (str, 'name')))
        i['series'] = split_ids(i['series'], ((int, 'id'), (str, 'name'), (int, 'serno')))
        i['genres'] = split_ids(i['genres'], ((int, 'id'), (str, 'name')))
        i['keywords'] = split_ids(i['keywords'], ((int, 'id'), (str, 'name')))

    endTime = time()
    return {
        'ok': True,
        'result': response,
        'parameters': parameters,
        'time': {
            'total': (time() - startTime) * 1000,
            'sql': (sqlEnd - sqlTime) * 1000,
            'processing': (endTime - sqlEnd) * 1000
        },
        'sql': sql
    }
