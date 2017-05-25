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
            'ok': fb2['ok'],
            'fb2': fb2['result'],
            'db': book
        }
    else:
        return fb2


def search(
        conn,
        book_id=None, author_id=None, serie_id=None, order=None,
        start=0, count=0, author=None, title=None, serie=None, genre=None,
        serno_min=None, serno_max=None, rate_min=None, rate_max=None, lang=None
):
    startTime = time()

    if not order and (count or start):
        order = 'ORDER BY b.book_id'
    elif not order:
        order = ''
    elif order in ['book_id', 'author_id', 'serie_id', 'rate', 'size', 'serno', 'title', 'authors']:
        order = 'ORDER BY b.' + order
    else:
        return {'ok': False, 'error': 'Unknown order'}

    params = {
        'limit': start + count if count else None,
        'book_id': book_id,
        'author_id': author_id,
        'serie_id': serie_id,
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

    sqlTime = time()
    sql = '''
        SELECT b.*, s.name AS serie
        FROM books b, series s
        WHERE b.serie_id = s.serie_id
        {book_id}
        {author_id}
        {serie_id}

        {lang}
        {serno_a} {serno_b}
        {rate_a} {rate_b}
        {title}
        {serie}
        {author}
        {genre}
        {order}
        {limit}
    '''.format(
        book_id='AND b.book_id=:book_id' if book_id else '',
        author_id='''
            AND b.book_id IN (
                SELECT book_id FROM author_to_book WHERE author_id=:author_id
            )''' if author_id else '',
        serie_id='AND b.serie_id=:serie_id' if serie_id else '',
        lang='AND b.lang=:lang' if lang else '',
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
                    AND name=:genre
            )''' if genre else '',
        order=order,
        limit='LIMIT :limit' if count else ''
    )
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
        # 'sql': sql
    }
