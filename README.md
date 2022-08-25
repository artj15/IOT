# IOT

## Запуск ДБ и применение миграций:

docker-compose up dbmate

## Запуск тестов:

docker-compose run iot_app pytest tests

## Запуск сервиса:

docker-compose up

## Решение:

Для решения задачи использовался стек:

    - Docker-compose
    - PostgreSQL
    - FastApi
    - AsyncPg
    - Asyncio
    - Pandas
    - Redis

При решении задачи возникли проблемы при открытии .csv файла, поэтому было принято решение изменить сепаратор на
regex-выражение и движок с 'c' на 'python', изменить тип колонки, для расчёта суммы, на float.
