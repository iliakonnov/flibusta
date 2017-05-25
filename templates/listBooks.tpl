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
                        <td>
                            {% set authors=book['authors'].split(':') %}
                                {% for author in authors[:-1] %}
                                    {% if author %}
                                        <a href="/search?author={{author}}">{{author.replace(',', ' ').rstrip(' ')}}</a>, 
                                    {% endif %}
                                {% endfor %}
                                {{ authors[-1].replace(',', ' ').rstrip(' ') }}
                            {# {% endset %} #}
                        </td>
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
                            {% set genres=book['genres'].split(':') %}
                                {% for genre in genres[:-1] %}
                                    {% if genre %}
                                        {{ genres_translation[genre] }}, 
                                    {% endif %}
                                {% endfor %}
                                {{ genres_translation[genres[-1]] }}
                            {# {% endset %} #}
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