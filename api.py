from time import time
from fb2reader import getBook as getFb2

def getBook(conn, zippath, book_id=None, file_id=None):
    if not file_id:
        books = conn.execute(
            'SELECT file FROM books WHERE book_id=?',
            (book_id,)
        ).fetchone()
        if books:
            file_id = books[0]
        else:
            return {
                'ok': False,
                'error': 'Book not found'
            }

    return getFb2(file_id, zippath)


def search(
        conn,
        start=0, count=0, author=None, title=None, serie=None, genre=None,
        serno_min=None, serno_max=None, rate_min=None, rate_max=None, lang=None
):
    startTime = time()

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

    sqlTime = time()
    sql = '''
        WITH sel_books AS (
            SELECT b.*, s.name AS serie
            FROM books b, series s
            WHERE b.serie_id = s.serie_id
            {lang}
            {serno_a} {serno_b}
            {rate_a} {rate_b}
            {title}
            {serie}
        ),
        list_authors AS (
            SELECT b.book_id, GROUP_CONCAT(a.name, ':') AS author_list
            FROM authors a, author_to_book b
            WHERE a.author_id = b.author_id
            GROUP BY b.book_id
        ),
        list_genres AS (
            SELECT b.book_id, GROUP_CONCAT(g.name, ':') AS genre_list
            FROM genres g, genre_to_book b
            WHERE g.genre_id = b.genre_id
            GROUP BY b.book_id
        )
        SELECT sel_books.*
        FROM sel_books
        WHERE 1=1
        {author}
        {genre}
        {order}
        {limit}
    '''.format(
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
            AND sel_books.book_id IN (
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
            AND sel_books.book_id IN (
                SELECT b.book_id
                FROM genres g, genre_to_book b
                WHERE g.genre_id = b.genre_id
                    AND name=:genre
            )''' if genre else '',
        order='ORDER BY sel_books.book_id' if count or start else '',
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
        'result': response,
        'parameters': parameters,
        'time': {
            'total': (time() - startTime) * 1000,
            'sql': (sqlEnd - sqlTime) * 1000,
            'processing': (endTime - sqlEnd) * 1000
        },
        # 'sql': sql
    }
