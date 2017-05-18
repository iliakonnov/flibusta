#!/usr/bin/python3.6
# -*- coding: utf8 -*-
import os
import codecs
import sqlite3
from zipfile import ZipFile
from lxml import etree
xmlns = '{http://www.gribuser.ru/xml/fictionbook/2.0}'


def getBook(fileName, zipPath):
    zipId, bookId = fileName.split('/')[-2:]
    zipId = zipId.rstrip('.inp')
    with ZipFile(os.path.join(zipPath, zipId + '.zip'), 'r') as z:
        book = z.read(bookId + '.fb2')
        root = etree.XML(book)
        info = root.find("{xmlns}description/{xmlns}title-info".format(xmlns=xmlns))

        imageElem = root.find('./{xmlns}binary'.format(xmlns=xmlns))
        if imageElem is not None:
            image = codecs.decode(imageElem.text.encode('utf-8'), 'base64')
            imageMime = imageElem.get('content-type')
        else:
            image = None
            imageMime = None

        annotationElem = info.find("./{xmlns}annotation".format(xmlns=xmlns))
        if annotationElem is not None:
            annotation = ''.join([
                i for i in annotationElem.itertext()
                if i.strip('\n').strip(' ')
            ])
        else:
            annotation = None

        langElem = info.find("./{xmlns}lang".format(xmlns=xmlns))
        if langElem is not None:
            lang = langElem.text
        else:
            lang = None

        author_info = info.find("./{xmlns}author".format(xmlns=xmlns))
        lastname = info.find("./{xmlns}author/{xmlns}last-name".format(xmlns=xmlns))
        middlename = info.find("./{xmlns}author/{xmlns}middle-name".format(xmlns=xmlns))
        firstname = info.find("./{xmlns}author/{xmlns}first-name".format(xmlns=xmlns))
        author = {
            'firstname': firstname.text if firstname is not None else None,
            'middlename': middlename.text if middlename is not None else None,
            'lastname': lastname.text if lastname is not None else None
        }

        ser_info = info.find("./{xmlns}sequence".format(xmlns=xmlns))
        if ser_info is not None:
            serie = ser_info.get('name')
            serno = ser_info.get('number')
        else:
            serie = None
            serno = None

        pubInfo = root.find("{xmlns}description/{xmlns}publish-info".format(xmlns=xmlns))
        if pubInfo is not None:
            '''
            <book-name>Первый из могикан</book-name>
            <publisher>Эксмо</publisher>
            <city>Москва</city>
            <year>2006</year>
            <isbn>5-699-15149-4</isbn>
            <sequence name="Русская фантастика" number="0" />
            '''
            pubInfoElems = {
                'bookName': pubInfo.find("./{xmlns}book-name".format(xmlns=xmlns)),
                'publisher': pubInfo.find("./{xmlns}publisher".format(xmlns=xmlns)),
                'city': pubInfo.find("./{xmlns}city".format(xmlns=xmlns)),
                'year': pubInfo.find("./{xmlns}year".format(xmlns=xmlns)),
                'isbn': pubInfo.find("./{xmlns}isbn".format(xmlns=xmlns)),
                'sequenceName': pubInfo.find("./{xmlns}sequence".format(xmlns=xmlns)),
                'sequenceNum': pubInfo.find("./{xmlns}sequence".format(xmlns=xmlns))
            }

            publishInfo = {
                'bookName': publishInfoElems['bookName'].text if pubInfoElems['bookName'] is not None else None,
                'publisher': pubInfoElems['publisher'].text if pubInfoElems['publisher'] is not None else None,
                'city': pubInfoElems['city'].text if pubInfoElems['city'] is not None else None,
                'year': pubInfoElems['year'].text if pubInfoElems['year'] is not None else None,
                'isbn': pubInfoElems['isbn'].text if pubInfoElems['isbn'] is not None else None,
                'sequenceName': pubInfoElems['sequenceName'].get('name') if pubInfoElems['sequenceName'] is not None else None,
                'sequenceNum': pubInfoElems['sequenceNum'].get('number') if pubInfoElems['sequenceNum'] is not None else None
            }
        else:
            publishInfo = None

        return {
            'bookId': bookId,
            'book': book,
            'image': image,
            'imageMime': imageMime,
            'annotation': annotation,
            'lang': lang,
            'author': author,
            'publish_info': publishInfo,
            'serie': serie,
            'serno': serno,
            'author': author
        }

if __name__ == "__main__":
    from pprint import pprint
    from sys import argv
    from mimetypes import guess_extension
    result = getBook(argv[1], argv[2])
    pprint(
        {x: result[x] for x in result if x not in ('book', 'image')}
    )

    with open(result['bookId'] + '.fb2', 'wb') as f:
        f.write(result['book'])

    if result['image'] is not None:
        if result['imageMime'] is not None:
            imgExt = guess_extension(result['imageMime'])
        else:
            imgExt = '.cover'
        with open(result['bookId'] + imgExt, 'wb') as f:
            f.write(result['image'])