# IOT

## Запуск ДБ и применения миграций:

docker-compose up dbmate

## Запуск тестов:

docker-compose run iot_app pytest tests

## Запуск сервиса:

docker-compose up

## Решение:

Для решения задачи использовался стек:

    - PostgreSQL
    - FastApi
    - AsyncPg
    - Pandas
    - Redis

При решении задачи возникли проблемы при открытии .csv файла, поэтому было принято решение изменить сепаратор на
regex-выражение и движок с 'c' на 'python', изменить тип суммируещей колонки на float.
