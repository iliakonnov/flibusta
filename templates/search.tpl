<div id="alert" class="alert alert-warning" hidden="hidden">
    Необходимо указать либо название книги, либо имя автора, либо имя серии
</div>
<form id="form" class="form" action="/search">
    <div class="list-group">
        <div class="list-group-item">
            <div class="input-group">
                <input type="text" name="title" class="form-control input-lg" placeholder="Поиск книги по названию" />
                <span class="input-group-btn">
                        <button class="btn btn-primary btn-lg" type="submit">
                            <i class="glyphicon glyphicon-search"></i>
                        </button>
                    </span>
            </div>
        </div>
        <div class="list-group-item">
            <button id="showAdvanced" class="btn btn-sm" type="button">
                <span>Расширенный поиск</span>
            </button>
        </div>
        <div id="advanced" style="display: none;">
            <div class="list-group-item">
                <input type="text" name="author" class="form-control input-lg" placeholder="Имя автора" />
            </div>
            <div class="list-group-item">
                <input type="text" name="serie" class="form-control input-lg" placeholder="Название серии" />
            </div>
            <div class="list-group-item">
                <select id="genres" type="text" name="genre" class="form-control input-lg">
                    <option value="" selected>Жанр книги</option>
                    <!-- Тут должны быть жанры, которые заполняет js на основе словаря-->
                </select>
            </div>
            <div class="list-group-item">
                <table class="table table-condensed searchTable"><tr>
                    <td class="smallTd">
                        <input type="number" name="serno_min" min="-1" class="form-control input-lg" placeholder="min" />
                    </td>
                    <td class="bigTd">
                        <p class="lead text-nowrap text-center">&ge; номер в серии &ge;</p>
                    </td>
                    <td class="smallTd">
                        <input type="number" name="serno_max" min="-1" class="form-control input-lg" placeholder="max" />
                    </td>
                </tr></table>
            </div>
            <div class="list-group-item">
                <table class="table table-condensed searchTable"><tr>
                    <td class="smallTd">
                        <input type="number" name="rate_min" min="-1" class="form-control input-lg" placeholder="min" />
                    </td>
                    <td class="bigTd">
                        <p class="lead text-nowrap text-center">&ge; рейтинг &ge;</p>
                    </td>
                    <td class="smallTd">
                        <input type="number" name="rate_max" min="-1" class="form-control input-lg" placeholder="max" />
                    </td>
                </tr></table>
            </div>
            <div class="list-group-item">
                <select id="languages" type="text" name="lang" class="form-control input-lg">
                    <option value="" disabled selected>Язык книги</option>
                    <!-- Тут должны быть языки, которые заполняет js на основе словаря-->
                </select>
            </div>
            <div class="list-group-item">
                <button class="btn btn-block btn-primary btn-lg" type="submit">Найти</button>
            </div>
        </div>
    </div>
</form>
<script src="/index.js"></script>