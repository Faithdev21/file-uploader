# File uploader Project

Документация (доступна после запуска проекта):

http://127.0.0.1/swagger/

http://127.0.0.1/redoc/

Проект упакован в контейнеры Docker для локального запуска.

---

### Технологии

Python 3.9, Django 4.2, DRF 3.14, Docker, PostgreSQL 13.0, Gunicorn 21.2, Nginx 1.21, Celery 5.2.2, Redis 5.0.1

---

### Запуск проекта локально

Склонируйте репозиторий:

```git@github.com:Faithdev21/file-uploader.git```

либо

```https://github.com/Faithdev21/file-uploader.git```

Добавьте файл с названием .env в backend/cookbook (туда же, где .env.example) и заполните его:

```
SECRET_KEY=django-insecure-r7=j=j2^+d-vx(rm%0wpa7b!r5t#wb#yeffoq2#co*^2(pg2oy
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,backend
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Из директории с docker-compose.yaml выполните:

```docker-compose up -d```

Для пересборки образа (в случае обновления содержимого проекта) дополните команду так:

```docker-compose up -d --build```

Примените миграции:

```docker-compose exec backend python manage.py migrate```

Создайте суперюзера:

```docker-compose exec backend python manage.py createsuperuser```

---

### Основной функционал:

`http://127.0.0.1/api/files/`  

GET - Получение списка всех загруженных файлов.

`http://127.0.0.1/api/upload/`

POST - Загружает файл с последующей его обработкой.

---

### Дополнительный функционал:

`http://127.0.0.1/index/`

Генерация html страницы со всеми загруженными файлами

---

### Тестирование:

Запустите тесты:

```docker-compose exec backend coverage run manage.py test```

Результаты тестирования:

```docker-compose exec backend coverage report```

(Покрытие тестами - 93%)  
![image](https://github.com/Faithdev21/file-uploader/assets/119350657/bbead4d1-29bb-477a-bb17-a30d262e5da3)

---

### Примечания по усложнениям:

**При ожидании большой нагрузки может помочь:**
1. Настройка буферов Nginx в соответствии с ожидаемой нагрузкой
2. Настройка индексов БД
3. Горизонтальное масштабирование (например использование Kubernetes)
4. Использование кэширования
5. Использование облачного хранилища
6. Использование асинхронного фреймворка (например FastAPI)

**Нагрузка на сервис при 1000 запросах (при 10 одновременных запросах):**
1. 300 RPS, эндпоинт api/uploads с небольшим текстовым файлом в теле запроса (без потерь)
2. 98 RPS, эндпоинт api/files (без потерь)

**Нагрузка на сервис при 100 000 запросах (при 100 одноврменных запросах):**
1. 298 RPS, эндпоинт api/uploads с небольшим текстовым файлом в теле запроса (без потерь)
2. 96 RPS, эндпоинт api/files (без потерь)

**Нагрузка на сервис при 100 000 запросах (при 1000 одноврменных запросах):**
1. 711 RPS, эндпоинт api/uploads с небольшим текстовым файлом в теле запроса (94% потерь)
2. 1086 RPS, эндпоинт api/files (80% потерь)
   
---

Документация API:

http://127.0.0.1/swagger/

http://127.0.0.1/redoc/

### Автор проекта

Егор Лоскутов

https://github.com/Faithdev21
