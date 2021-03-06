### Описание проекта:

```
Yamdb — сервис-отзовик. Проект собирает отзывы пользователей на произведения. 
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».Список категорий может быть расширен администратором.
В каждой категории есть произведения: книги, фильмы или музыка. 
Произведению может быть присвоен жанр. Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы.
Стек технологий: python, django, DRF, git, sqlite
```

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:pkrfc/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов:

```
Запрос:
GET http://127.0.0.1:8000/api/v1/categories/
Ответ:
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]

```

```
Запрос:
GET http://127.0.0.1:8000/api/v1/genres/
Ответ:
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
