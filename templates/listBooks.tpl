<div>
    {% for book in books %}
        <div class="card card-sm">
            <div class="card-header">
                <h5 class="card-title">
                    {% if book['deleted'] %}<s>{% endif %}
                    <a class="card-title" href="/book/{{ book['book_id'] }}" target="_blank">{{ book['title'] }}</a>
                    {% if book['title_alt'] %}{{ book['title_alt'] }}{% endif %}
                    {% if book['deleted'] %}</s>{% endif %}
                </h5>
            </div>
            <div class="card-body">
                <p class="card-text">
                <div class="row info{{ book['book_id'] }} collapse show">
                    <div class="col-md-5">
                        {% if book['authors'] %}
                            <b>Автор:</b>
                            <a href="/search?author_id={{ book['authors'][0]['id'] }}">
                                {{ book['authors'][0]['name'].replace(',', ' ').rstrip(' ') }}
                            </a>
                            {% if book['authors'] | length > 1 %}
                                и др.
                            {% endif %}
                        {% endif %}
                    </div>
                    <div class="col-md-5">
                        {% if book['series'] %}
                            №{{ book['series'][0]['serno'] }} в серии
                            <a href="/search?order=serno&serie_id={{ book['series'][0]['id'] }}">
                                {{ book['series'][0]['name'] }}
                            </a>
                            {% if book['series'] | length > 1 %}
                                и др.
                            {% endif %}
                        {% endif %}
                    </div>
                    <div class="col-md-1">
                        {% if book['lang'] != 'ru' %}
                            <mark>{{ book['lang'] }}</mark>
                        {% endif %}
                    </div>
                    <button
                            class="btn btn-sm col-md-1"
                            type="button"
                            data-toggle="collapse"
                            data-target=".info{{ book['book_id'] }}"
                            aria-expanded="false"
                            aria-controls="multiCollapseExample1 multiCollapseExample2">
                        Подробно
                    </button>
                </div>
                <div class="row info{{ book['book_id'] }} collapse">
                    <div class="col-md-11">
                        {% if book['joined_into'] %}
                            Книга объединена с <a href="/search?book_id={{ book['joined_into'] }}">другой</a>
                        {% endif %}

                        <div>
                            <b>Авторы:</b>
                            <ul>
                                {% for a in book['authors'] %}
                                    <li>
                                        <a href="/search?author_id={{ a['id'] }}">{{ a['name'].replace(',', ' ').rstrip(' ') }}</a>
                                    </li>
                                {% endfor %}
                            </ul>
                        </div>

                        {% if book['series'] %}<div>
                            <b>Серии:</b>
                            <ul>
                                {% for s in book['series'] %}
                                    <li>
                                        №{{ s['serno'] }} в <a href="/search?serie_id={{ s['id'] }}">{{ s['name'] }}</a>
                                    </li>
                                {% endfor %}
                            </ul>
                        </div>{% endif %}

                        {% if book['genres'] %}<div>
                            <b>Жанры:</b>
                            <ul class="inline-list">
                                {% for g in book['genres'] %}
                                    <li>
                                        <a href="/search?count=30&genre_id={{ g['id'] }}">{{ genres_translation[g['name']] }}</a>
                                    </li>
                                {% endfor %}
                            </ul>
                        </div>{% endif %}

                        {% if book['keywords'] %}<div>
                            <b>Ключевые слова:</b>
                            <ul class="inline-list">
                                {% for kw in book['keywords'] %}
                                    <li>
                                        <a href="/search?count=30&keyword_id={{ kw['id'] }}">{{ kw['name'] }}</a>
                                    </li>
                                {% endfor %}
                            </ul>
                        </div>{% endif %}

                        <div><b>Язык:</b> <code>{{ book['lang'] }}</code> </div>
                        {% if book['rate'] != None and book['rate'] != -1 %}
                            <div><b>Рейтинг:</b> {{ book['rate'] }}</div>
                        {% endif %}
                    </div>
                    <div class="col-md-1">
                        <button
                                class="btn btn-sm"
                                type="button"
                                data-toggle="collapse"
                                data-target=".info{{ book['book_id'] }}"
                                aria-expanded="false"
                                aria-controls="multiCollapseExample1 multiCollapseExample2">
                            Кратко
                        </button>
                    </div>
                </div>
                </p>
            </div>
        </div>
    {% endfor %}
</div>
