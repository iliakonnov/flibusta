{% set genres_translation= {"sci_textbook":"Учебники и пособия","religion_protestantism":"Протестантизм","religion_catholicism":"Католицизм","sf_social":"Социально-психологическая фантастика","prose_classic":"Классическая проза","sf_detective":"Детективная фантастика","ref_encyc":"Энциклопедии","reference":"Справочная литература","sci_geo":"Геология и география","detective":"Детективы","foreign_children":"Зарубежная литература для детей","poetry_classical":"Классическая поэзия","cine":"Кино","child_prose":"Проза для детей","antique_east":"Древневосточная литература","child_education":"Детская образовательная литература","home_crafts":"Хобби и ремесла","prose_history":"Историческая проза","sf_space":"Космическая фантастика","sci_metal":"Металлургия","sci_history":"История","sci_tech":"Технические науки","det_su":"Советский детектив","sf_humor":"Юмористическая фантастика","comp_db":"Программирование, программы, базы данных","antique":"antique","design":"Искусство и Дизайн","adv_history":"Исторические приключения","sf":"Научная Фантастика","home_entertain":"Развлечения","religion_paganism":"Язычество","antique_russian":"Древнерусская литература","popular_business":"Карьера, кадры","child_classical":"Классическая детская литература","fanfiction":"Фанфик","modern_tale":"Современная сказка","love_sf":"Любовное фэнтези, любовно-фантастические романы ","antique_myths":"Мифы. Легенды. Эпос","lyrics":"Лирика","religion_orthodoxy":"Православие","child_verse":"Стихи для детей","song_poetry":"Песенная поэзия","love_short":"Короткие любовные романы","love_history":"Исторические любовные романы","home":"Домоводство","prose_su_classics":"Советская классическая проза","sf_epic":"Эпическая фантастика","love_hard":"Порно","sci_psychology":"Психология и психотерапия","literature_18":"Классическая проза XVII-XVIII веков","det_classic":"Классический детектив","adv_geo":"Путешествия и география","sci_economy":"Экономика","comp_hard":"Компьютерное 'железо' (аппаратное обеспечение), цифровая обработка сигналов","humor_prose":"Юмористическая проза","tbg_school":"Школьные учебники и пособия, рефераты, шпаргалки","tbg_computers":"Учебные пособия, самоучители","adv_modern":"Приключения в современном мире","sci_oriental":"Востоковедение","det_maniac":"Про маньяков","religion":"Религия, религиозная литература","poetry_rus_classical":"Классическая русская поэзия","poetry_for_modern":"Современная зарубежная поэзия","geo_guides":"Путеводители, карты, атласы ","home_pets":"Домашние животные","det_police":"Полицейский детектив","children":"Детская литература","sci_juris":"Юриспруденция","economics_ref":"Деловая литература","child_sf":"Фантастика для детей","sci_biology":"Биология, биофизика, биохимия ","comp_www":"ОС и Сети, интернет","palindromes":"Визуальная и экспериментальная поэзия, верлибры, палиндромы","sf_postapocalyptic":"Постапокалипсис","sci_chem":"Химия","ref_ref":"Справочники","auto_regulations":"Автомобили и ПДД","prose_counter":"Контркультура","prose_contemporary":"Современная русская и зарубежная проза","great_story":"Роман, повесть","child_folklore":"Детский фольклор","sci_philosophy":"Философия","tbg_higher":"Учебники и пособия ВУЗов","aphorisms":"Афоризмы, цитаты","foreign_prose":"Зарубежная классическая проза","ref_dict":"Словари","thriller":"Триллер","humor":"Юмор","home_diy":"Сделай сам","home_cooking":"Кулинария","military_history":"Военная история","religion_islam":"Ислам","other":"Неотсортированное","russian_fantasy":"Славянское фэнтези","home_collecting":"Коллекционирование","sci_ecology":"Экология","sci_politics":"Политика","literature_19":"Классическая проза ХIX века","military_special":"Военное дело","sci_culture":"Культурология","epistolary_fiction":"Эпистолярная проза","tragedy":"Трагедия","sf_mystic":"Мистика","sf_fantasy":"Фэнтези","prose_rus_classic":"Русская классическая проза","child_det":"Детская остросюжетная литература","ref_guide":"Руководства","foreign_antique":"Средневековая классическая проза","prose":"Проза","sci_veterinary":"Ветеринария","humor_verse":"Юмористические стихи, басни ","gothic_novel":"Готический роман","poetry":"Поэзия","tbg_secondary":"Учебники и пособия для среднего и специального образования","prose_magic":"Магический реализм","sf_horror":"Ужасы","sf_cyberpunk":"Киберпанк","religion_hinduism":"Индуизм","det_political":"Политический детектив","sf_stimpank":"Стимпанк","humor_anecdote":"Анекдоты","astrology":"Астрология и хиромантия","sci_religion":"Религиоведение","poem":"Поэма, эпическая поэзия","proverbs":"Пословицы, поговорки","nonf_military":"Военная документалистика и аналитика","fairy_fantasy":"Мифологическое фэнтези","prose_game":"Игры, упражнения для детей","home_sex":"Семейные отношения, секс","det_action":"Боевик","folk_songs":"Народные песни","limerick":"Частушки, прибаутки, потешки","child_tale_rus":"Русские сказки","poetry_for_classical":"Классическая зарубежная поэзия","org_behavior":"Маркетинг, PR","sf_action":"Боевая фантастика","art_criticism":"Искусствоведение","literature_20":"Классическая проза ХX века","tale_chivalry":"Рыцарский роман","periodic":"Журналы, газеты ","equ_history":"История техники","sci_radio":"Радиоэлектроника","auto_business":"Автодело","humor_satire":"Сатира","comedy":"Комедия","drama":"Драма","sci_build":"Строительство и сопромат","sci_linguistic":"Языкознание, иностранные языки","folklore":"Фольклор, загадки folklore","nonf_biography":"Биографии и Мемуары","art_world_culture":"Мировая художественная культура","religion_judaism":"Иудаизм","det_espionage":"Шпионский детектив","sci_medicine_alternative":"Альтернативная медицина","adv_maritime":"Морские приключения","sci_phys":"Физика","sci_zoo":"Зоология","sci_medicine":"Медицина","prose_neformatny":"Экспериментальная, неформатная проза","religion_christianity":"Христианство","det_crime":"Криминальный детектив","nonf_criticism":"Критика","vaudeville":"Мистерия, буффонада, водевиль","sci_state":"Государство и право","poetry_modern":"Современная поэзия","travel_notes":"География, путевые заметки","music":"Музыка","love_contemporary":"Современные любовные романы","love":"Любовные романы","sci_math":"Математика","antique_european":"Европейская старинная литература","sci_popular":"Зарубежная образовательная литература, зарубежная прикладная,  научно-популярная  литература","notes":"Партитуры","comics":"Комиксы","painting":"Живопись, альбомы, иллюстрированные каталоги","home_health":"Здоровье","prose_abs":"Фантасмагория, абсурдистская проза","home_garden":"Сад и огород","sf_fantasy_city":"Городское фэнтези","home_sport":"Боевые искусства, спорт ","banking":"Финансы","sci_social_studies":"Обществознание, социология","economics":"Экономика","sf_technofantasy":"Технофэнтези","screenplays":"Сценарий","epic":"Былины, эпопея","antique_ant":"Античная литература","computers":"Зарубежная компьютерная, околокомпьютерная литература ","poetry_east":"Поэзия Востока","nonf_publicism":"Публицистика","religion_esoterics":"Эзотерика, эзотерическая литература ","adventure":"Приключения","hronoopera":"Хроноопера","det_history":"Исторический детектив","drama_antique":"Античная драма","science":"Научная литература","family":"Семейные отношения","sci_botany":"Ботаника","sf_litrpg":"ЛитРПГ","religion_self":"Самосовершенствование","sci_cosmos":"Астрономия и Космос","military_weapon":"Военное дело, военная техника и вооружение","sci_philology":"Литературоведение","child_adv":"Приключения для детей и подростков","network_literature":"Самиздат, сетевая литература","poetry_rus_modern":"Современная русская поэзия","adv_animal":"Природа и животные","sci_theories":"Альтернативные науки и научные теории","sf_etc":"Фантастика","nonfiction":"Документальная литература","love_erotica":"Эротическая литература","story":"Малые литературные формы прозы: рассказы, эссе, новеллы, феерия","theatre":"Театр","child_tale":"Сказки народов мира","det_irony":"Иронический детектив, дамский детективный роман","religion_budda":"Буддизм","architecture_book":"Скульптура и архитектура","sf_history":"Альтернативная история, попаданцы","love_detective":"Остросюжетные любовные романы","det_hard":"Крутой детектив","adv_indian":"Вестерн, про индейцев ","dramaturgy":"Драматургия","unfinished":"Незавершенное","sci_transport":"Транспорт и авиация","sci_pedagogy":"Педагогика, воспитание детей, литература для родителей ","prose_military":"Проза о войне","sf_heroic":"Героическая фантастика","folk_tale":"Народные сказки"} %}

<div class="panel-group">
    {% for book in books %}
        <div class="panel panel-default">
            <div class="panel-heading">
                <a href="/book/{{ book['book_id'] }}" target="_blank">{{book['title']}}</a>
            </div>
            <div class="panel-body">
                <table class="table">
                    <tr>
                        <td class="col-md-2">Название</td>
                        <td>{{ book['title'] }}</td>
                    </tr>
                    <tr>
                        <td class="col-md-2">Авторы</td>
                        <td>{{ book['authors'].replace(',', ' ').replace(':', ', ').rstrip(', ') }}</td>
                    </tr>
                    {% if book['serie'] %}
                    <tr>
                        <td class="col-md-2">Серия книг</td>
                        <td><a href="/serie/{{ book['serie_id'] }}">{{ book['serie'] }}</a> <b>(№{{ book['serno'] }})</b></td>
                    </tr>
                    {% endif %}
                    <tr>
                        <td class="col-md-2">Жанры</td>
                        <td>
                            {% for genre in book['genres'].split(':') %}
                                {% if genre %}
                                    {{ genres_translation[genre] + ',' }}
                                {% endif %}
                            {% endfor %}
                        </td>
                    </tr>
                    {% if book['rate'] != -1 %}
                    <tr>
                        <td class="col-md-2">Рейтинг</td>
                        <td>{{ book['rate'] }}</td>
                    </tr>
                    {% endif %} {% if book['keywords'] %}
                    <tr>
                        <td class="col-md-2">Ключевые слова</td>
                        <td>{{ book['keywords'] }}</td>
                    </tr>
                    {% endif %}
                    <tr>
                        <td class="col-md-2">Язык</td>
                        <td>{{ book['lang'] }}</td>
                    </tr>
                </table>
            </div>
        </div>
    {% endfor %}
</div>