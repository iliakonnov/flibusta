Web API поиска по библиотеке
============================

Поиск книги (/search)
-----------

### Параметры запроса
Обязательно должно выполнятся хотя бы одно из условий:
1. **count** < 1000
2. **author**, **title**, **serie**, **genre**: есть хотя бы один alphanumeric символ

* **start**: Для разделения по страницам, кол-во книг, которые надо пропустить
* **count**: Кол-во книг, которые надо получить
* **author**: Имя автора книги (можно использоваать wildcard FTS)
* **title**: Название книги (можно использоваать wildcard FTS)
* **serie**: Название серии, в которую входит эта книга. (можно использоваать wildcard FTS)
* **genre**: Точное название жанра fb2 (список: http://flisland.net/g)
* **serno_min**: Минимальный номер книги в серии (включительно)
* **serno_max**: Максимальный номер книги в серии (включительно)
* **rate_min**: Минимальный рейтинг книги (включительно)
* **rate_max**: Максимальный рейтинг книги (включительно)
* **lang**: Язык книги. Например: ru, en, cs и т.д.

### Результат
Возвращается json с тремя ключами:
* **parameters**: Список параметров запроса в виде словаря
* **time**: Словарь, хранящий время выполнения запроса в секундах
    - **processing**: Время, потраченное на обработку результата
    - **sql**: Время, потраченное на получение данных из БД
    - **total**: Общее время, может быть не равно сумме двух других
* **result**: Сам результат поиска.
    - **add_date**: Время добавления книги
    - **authors**: Список авторов книги, разделённых двоеточием
    - **book_id**: ID книги
    - **file**: Путь к файлу из которого была получена информация о книге и ID книги
    - **genres**: Список жанров, разделённых двоеточием
    - **keywords**: Ключевые слова книги, могут быть разделены чем угодно
    - **lang**: Язык книги, две буквы
    - **rate**: Рейтинг книги, если его нет, то `-1`
    - **serie**: Серия, в которую входит книга. Если книга не входит в какую лиюо серию, то пустая строка
    - **serie_id**: ID серии.
    - **serno**: Номер книги в серии, если книга не входит ни в одну серию, то `-1`
    - **size**: Размер файла книги в байтах
    - **title**: Название книги

Получение книги (/get)
---------------

### Параметры запроса
Обязательно должен быть хотя бы один из параметров
* **book_id**: ID книги, которую надо получить. Работает немного медленнее
* **file**: Путь к файлу из которого была получена информация.

### Результат
Возвращается json. Любой из параметров, кроме `book_id` и `book` может быть null. Информация может не совпадать с информацией в базе.
* **annotation**: Аннотация к книге
* **author**: Информация об авторе
    - **firstname**: Имя
    - **lastname**: Фамилия
    - **middlename**: Отчество
* **book**: fb2 книги, закодированный в base64
* **book_id**: ID книги
* **image**: Обложка книги, закодированная в base64
* **imageMime**: mime-type формата обложки
* **lang**: Язык книги
* **publish_info**: Информация об издании.
    - **bookName**: Название книги
    - **city**: Город, где издано
    - **isbn**: ISBN книги
    - **publisher**: Название издательства
    - **sequenceName**: Название серии
    - **sequenceNum**: Номер книги в серии
    - **year**: Год издания
* **serie**: Название серии
* **serno**: Номер книги в серии