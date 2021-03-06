# Задание

### Вопрос №1
У вас SQL база с таблицами:
1) Users(userId, age)
2) Purchases (purchaseId, userId, itemId, date)
3) Items (itemId, price).

Напишите SQL запросы для расчета следующих метрик:
А) какую сумму в среднем в месяц тратит:
- пользователи в возрастном диапазоне от 18 до 25 лет включительно
- пользователи в возрастном диапазоне от 26 до 35 лет включительно
Б) в каком месяце года выручка от пользователей в возрастном диапазоне 35+ самая большая
В) какой товар обеспечивает дает наибольший вклад в выручку за последний год 
Г) топ-3 товаров по выручке и их доля в общей выручке за любой год

### Решение:
* Используем СУБД: PostgreSQL
В репозитории находится файл test_sql.sql
В нем находится код для создания таблиц, наполнения их тестовыми данными, а так же необходимые запросы к ним, обозначенные в тз.
Все тестировалось на https://extendsclass.com/postgresql-online.html

### Вопрос №2

С сайта google news (https://news.google.com) (язык и регион - English | United States) необходимо
прокачать все статьи за последний месяц (на момент прокачки) с ключевым словом Russia.
Затем для скачанных статей необходимо рассчитать топ-50 наиболее частотных слов и представить их в
виде word (tag) cloud. Данное задание необходимо выполнить с помощью python. Для представления в
виде word cloud можно использовать уже существующие библиотеки. Пример word cloud можно
посмотреть по ссылке -
https://altoona.psu.edu/sites/altoona/files/success-word-cloud.jpg

### Решение:
В репозитории находится файл parse_google.py
В нем расположен скрипт, включающий в себя парсинг ссылок новостей с news.google.com по заданным в тз параметрам, парсинг текста статей, работа над ним(очистка от лишних символов), а так же формирование word cloud, все подкреплено поясняющими комментариями.

Запуск программы (на примере Linux)
Создайте на своем компютере папку проекта mkdir parse_google и перейдите в нее cd parse_google
Склонируйте этот репозиторий в текущую папку https://github.com/DmitriyLush/test_task.git
Создайте виртуальное окружение python3 -m venv venv
Активируйте виртуальное окружение source venv/bin/activate
Установите зависимости pip3 install -r requirements.txt
Запустите программу python3 parse_google.py

### Вопрос №3

Представьте, что перед вами поставлена задача - создать инструмент для выделения нецензурной брани
в текстах. Как вы будете ее решать? Какие подходы, инструменты будете использовать? Попробуйте
описать основные этапы решения данной задачи? Как будете оценивать качество созданного
инструмента?

### Решение:
Т.к. с задачами из области nlp ранее не сталкивался, то первые мысли были о регулярных выражениях на каждое слово со всей возможной морфологией, границы для каждого выражения, чтобы исключить случаи, когда искомый набор букв - часть другого слова и словаре с исключениями, но с учетом богатства русского языка, и фантазии людей, я слабо себе представляю по-настоящему эффективный инструмент для этих целей. Можно коненчо дополнить стопслова в модуле nltk, и далее фильтровать текст с его помощью. Эффективность можно будет оценивать по скорости работы потенциального алгоритма, по его словарному запасу и способности понимать, что, условно, в формате нецензурной лексики, Банка == Б@нка и т.п.

