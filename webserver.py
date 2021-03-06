#!/usr/bin/python3.6
# -*- coding: utf8 -*-
import base64
import sqlite3
import api
import time
from flask import Flask, request, jsonify, abort, render_template, g

app = Flask(__name__, static_url_path='/static/')
app.config['JSON_AS_ASCII'] = False

GENRES_TRANSLATION = {"sci_textbook":"Учебники и пособия","religion_protestantism":"Протестантизм","religion_catholicism":"Католицизм","sf_social":"Социально-психологическая фантастика","prose_classic":"Классическая проза","sf_detective":"Детективная фантастика","ref_encyc":"Энциклопедии","reference":"Справочная литература","sci_geo":"Геология и география","detective":"Детективы","foreign_children":"Зарубежная литература для детей","poetry_classical":"Классическая поэзия","cine":"Кино","child_prose":"Проза для детей","antique_east":"Древневосточная литература","child_education":"Детская образовательная литература","home_crafts":"Хобби и ремесла","prose_history":"Историческая проза","sf_space":"Космическая фантастика","sci_metal":"Металлургия","sci_history":"История","sci_tech":"Технические науки","det_su":"Советский детектив","sf_humor":"Юмористическая фантастика","comp_db":"Программирование, программы, базы данных","antique":"antique","design":"Искусство и Дизайн","adv_history":"Исторические приключения","sf":"Научная Фантастика","home_entertain":"Развлечения","religion_paganism":"Язычество","antique_russian":"Древнерусская литература","popular_business":"Карьера, кадры","child_classical":"Классическая детская литература","fanfiction":"Фанфик","modern_tale":"Современная сказка","love_sf":"Любовное фэнтези, любовно-фантастические романы ","antique_myths":"Мифы. Легенды. Эпос","lyrics":"Лирика","religion_orthodoxy":"Православие","child_verse":"Стихи для детей","song_poetry":"Песенная поэзия","love_short":"Короткие любовные романы","love_history":"Исторические любовные романы","home":"Домоводство","prose_su_classics":"Советская классическая проза","sf_epic":"Эпическая фантастика","love_hard":"Порно","sci_psychology":"Психология и психотерапия","literature_18":"Классическая проза XVII-XVIII веков","det_classic":"Классический детектив","adv_geo":"Путешествия и география","sci_economy":"Экономика","comp_hard":"Компьютерное 'железо' (аппаратное обеспечение), цифровая обработка сигналов","humor_prose":"Юмористическая проза","tbg_school":"Школьные учебники и пособия, рефераты, шпаргалки","tbg_computers":"Учебные пособия, самоучители","adv_modern":"Приключения в современном мире","sci_oriental":"Востоковедение","det_maniac":"Про маньяков","religion":"Религия, религиозная литература","poetry_rus_classical":"Классическая русская поэзия","poetry_for_modern":"Современная зарубежная поэзия","geo_guides":"Путеводители, карты, атласы ","home_pets":"Домашние животные","det_police":"Полицейский детектив","children":"Детская литература","sci_juris":"Юриспруденция","economics_ref":"Деловая литература","child_sf":"Фантастика для детей","sci_biology":"Биология, биофизика, биохимия ","comp_www":"ОС и Сети, интернет","palindromes":"Визуальная и экспериментальная поэзия, верлибры, палиндромы","sf_postapocalyptic":"Постапокалипсис","sci_chem":"Химия","ref_ref":"Справочники","auto_regulations":"Автомобили и ПДД","prose_counter":"Контркультура","prose_contemporary":"Современная русская и зарубежная проза","great_story":"Роман, повесть","child_folklore":"Детский фольклор","sci_philosophy":"Философия","tbg_higher":"Учебники и пособия ВУЗов","aphorisms":"Афоризмы, цитаты","foreign_prose":"Зарубежная классическая проза","ref_dict":"Словари","thriller":"Триллер","humor":"Юмор","home_diy":"Сделай сам","home_cooking":"Кулинария","military_history":"Военная история","religion_islam":"Ислам","other":"Неотсортированное","russian_fantasy":"Славянское фэнтези","home_collecting":"Коллекционирование","sci_ecology":"Экология","sci_politics":"Политика","literature_19":"Классическая проза ХIX века","military_special":"Военное дело","sci_culture":"Культурология","epistolary_fiction":"Эпистолярная проза","tragedy":"Трагедия","sf_mystic":"Мистика","sf_fantasy":"Фэнтези","prose_rus_classic":"Русская классическая проза","child_det":"Детская остросюжетная литература","ref_guide":"Руководства","foreign_antique":"Средневековая классическая проза","prose":"Проза","sci_veterinary":"Ветеринария","humor_verse":"Юмористические стихи, басни ","gothic_novel":"Готический роман","poetry":"Поэзия","tbg_secondary":"Учебники и пособия для среднего и специального образования","prose_magic":"Магический реализм","sf_horror":"Ужасы","sf_cyberpunk":"Киберпанк","religion_hinduism":"Индуизм","det_political":"Политический детектив","sf_stimpank":"Стимпанк","humor_anecdote":"Анекдоты","astrology":"Астрология и хиромантия","sci_religion":"Религиоведение","poem":"Поэма, эпическая поэзия","proverbs":"Пословицы, поговорки","nonf_military":"Военная документалистика и аналитика","fairy_fantasy":"Мифологическое фэнтези","prose_game":"Игры, упражнения для детей","home_sex":"Семейные отношения, секс","det_action":"Боевик","folk_songs":"Народные песни","limerick":"Частушки, прибаутки, потешки","child_tale_rus":"Русские сказки","poetry_for_classical":"Классическая зарубежная поэзия","org_behavior":"Маркетинг, PR","sf_action":"Боевая фантастика","art_criticism":"Искусствоведение","literature_20":"Классическая проза ХX века","tale_chivalry":"Рыцарский роман","periodic":"Журналы, газеты ","equ_history":"История техники","sci_radio":"Радиоэлектроника","auto_business":"Автодело","humor_satire":"Сатира","comedy":"Комедия","drama":"Драма","sci_build":"Строительство и сопромат","sci_linguistic":"Языкознание, иностранные языки","folklore":"Фольклор, загадки folklore","nonf_biography":"Биографии и Мемуары","art_world_culture":"Мировая художественная культура","religion_judaism":"Иудаизм","det_espionage":"Шпионский детектив","sci_medicine_alternative":"Альтернативная медицина","adv_maritime":"Морские приключения","sci_phys":"Физика","sci_zoo":"Зоология","sci_medicine":"Медицина","prose_neformatny":"Экспериментальная, неформатная проза","religion_christianity":"Христианство","det_crime":"Криминальный детектив","nonf_criticism":"Критика","vaudeville":"Мистерия, буффонада, водевиль","sci_state":"Государство и право","poetry_modern":"Современная поэзия","travel_notes":"География, путевые заметки","music":"Музыка","love_contemporary":"Современные любовные романы","love":"Любовные романы","sci_math":"Математика","antique_european":"Европейская старинная литература","sci_popular":"Зарубежная образовательная литература, зарубежная прикладная,  научно-популярная  литература","notes":"Партитуры","comics":"Комиксы","painting":"Живопись, альбомы, иллюстрированные каталоги","home_health":"Здоровье","prose_abs":"Фантасмагория, абсурдистская проза","home_garden":"Сад и огород","sf_fantasy_city":"Городское фэнтези","home_sport":"Боевые искусства, спорт ","banking":"Финансы","sci_social_studies":"Обществознание, социология","economics":"Экономика","sf_technofantasy":"Технофэнтези","screenplays":"Сценарий","epic":"Былины, эпопея","antique_ant":"Античная литература","computers":"Зарубежная компьютерная, околокомпьютерная литература ","poetry_east":"Поэзия Востока","nonf_publicism":"Публицистика","religion_esoterics":"Эзотерика, эзотерическая литература ","adventure":"Приключения","hronoopera":"Хроноопера","det_history":"Исторический детектив","drama_antique":"Античная драма","science":"Научная литература","family":"Семейные отношения","sci_botany":"Ботаника","sf_litrpg":"ЛитРПГ","religion_self":"Самосовершенствование","sci_cosmos":"Астрономия и Космос","military_weapon":"Военное дело, военная техника и вооружение","sci_philology":"Литературоведение","child_adv":"Приключения для детей и подростков","network_literature":"Самиздат, сетевая литература","poetry_rus_modern":"Современная русская поэзия","adv_animal":"Природа и животные","sci_theories":"Альтернативные науки и научные теории","sf_etc":"Фантастика","nonfiction":"Документальная литература","love_erotica":"Эротическая литература","story":"Малые литературные формы прозы: рассказы, эссе, новеллы, феерия","theatre":"Театр","child_tale":"Сказки народов мира","det_irony":"Иронический детектив, дамский детективный роман","religion_budda":"Буддизм","architecture_book":"Скульптура и архитектура","sf_history":"Альтернативная история, попаданцы","love_detective":"Остросюжетные любовные романы","det_hard":"Крутой детектив","adv_indian":"Вестерн, про индейцев ","dramaturgy":"Драматургия","unfinished":"Незавершенное","sci_transport":"Транспорт и авиация","sci_pedagogy":"Педагогика, воспитание детей, литература для родителей ","prose_military":"Проза о войне","sf_heroic":"Героическая фантастика","folk_tale":"Народные сказки"}
PARAMS_TRANSLATION = {
    'start': 'Пропустить',
    'count': 'Кол-во книг',
    'author': 'Имя автора',
    'title': 'Название',
    'serie': 'Серия',
    'genre': 'Жанр',
    'rate_min': 'Минимальный рейтинг книги (включительно)',
    'rate_max': 'Максимальный рейтинг книги (включительно)',
    'lang': 'Язык',
    'book_id': 'ID книги',
    'author_id': 'ID автора',
    'serie_id': 'ID серии',
    'genre_id': 'ID жанра',
    'order': 'Сортировка',
}


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        conn = sqlite3.connect(app.config.get('dbpath'))
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

    book = api.getBook(get_db(), app.config.get('zippath'), book_id)

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


@app.route('/api/getAuthors')
def api_getAuthors():
    book_id = request.args.get('book_id', None)
    if not book_id:
        return abort(400)

    result = api.getAuthors(get_db(), book_id)
    if result['ok']:
        return jsonify(result['result'])
    else:
        return abort(400, result['error'])


@app.route('/api/getAuthorName')
def api_getAuthorName():
    author_id = request.args.get('author_id', None)
    if not author_id:
        return abort(400)

    result = api.getAuthorName(get_db(), author_id)
    if result['ok']:
        return jsonify(result['result'])
    else:
        return abort(400, result['error'])


@app.route('/api/getSerieName')
def api_getSerieName():
    serie_id = request.args.get('serie_id', None)
    if not serie_id:
        return abort(400)

    result = api.getSerieName(get_db(), serie_id)
    if result['ok']:
        return jsonify(result['result'])
    else:
        return abort(400, result['error'])


def do_search():
    args = dict(
        book_id = request.args.get('book_id', None),
        author_id = request.args.get('author_id', None),
        serie_id = request.args.get('serie_id', None),
        genre_id = request.args.get('genre_id', None),
        keyword_id = request.args.get('keyword_id', None),
        start = int(request.args.get('start', 0)),
        count = int(request.args.get('count', 0)),
        author = request.args.get('author', None),
        title = request.args.get('title', None),
        serie = request.args.get('serie', None),
        genre = request.args.get('genre', None),
        keyword = request.args.get('keyword', None),
        rate_min = request.args.get('rate_min', None),
        rate_max = request.args.get('rate_max', None),
        lang = request.args.get('lang', None),
        order = request.args.get('order', None),
    )

    if (
            args['book_id'] or args['author_id'] or args['serie_id'] or
            (args['count'] < 1000 and args['count'] > 0) or
            (args['author'] and [i for i in args['author'] if i.isalnum()]) or
            (args['title'] and [i for i in args['title'] if i.isalnum()]) or
            (args['serie'] and [i for i in args['serie'] if i.isalnum()])
    ):
        return api.search(
            get_db(),
            **args
        )
    else:
        return None


@app.route('/api/search')
def api_search():
    result = do_search()
    if result is None:
        return abort(400)
    elif result['ok']:
        return jsonify(dict([(k, v) for k, v in result.items() if k != 'ok']))
    else:
        return abort(400, result['error'])


@app.route('/book/<book_id>')
def bookInfo(book_id):
    book = api.getBook(get_db(), app.config.get('zippath'), book_id)
    if book['ok']:
        if isinstance(book['fb2'].get('image'), bytes):
            book['fb2']['image'] = base64.b64encode(book['fb2']['image']).decode('utf-8')
        if isinstance(book['fb2'].get('book'), bytes):
            book['fb2']['book'] = base64.b64encode(book['fb2']['book']).decode('utf-8')
        result = {
            'db': book['db'],
            'fb2': book['fb2']
        }
        return render_template(
            'book.html',
            book=result,
            genres_translation=GENRES_TRANSLATION,
            authors=api.getAuthors(get_db(), result['db']['book_id'])['result']
        )
    else:
        return render_template('searchError.html', error=book['error'])


@app.route('/search')
def search():
    result = do_search()
    if result is None:
        return render_template('searchError.html')
    elif result['ok']:
        return render_template(
            'search.html',
            genres_translation=GENRES_TRANSLATION,
            params_translation=PARAMS_TRANSLATION,
            result=result
        )
    else:
        return render_template('searchError.html', error=result['error'])


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
    app.config['zippath'] = argv[1]
    app.config['dbpath'] = argv[2] if len(argv) > 2 else 'data/flibusta.sqlite'
    app.run(host='0.0.0.0', debug=True)
