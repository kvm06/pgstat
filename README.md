# pgstat
Система сбора статистики по запросам в БД PostgreSQL
Итоговый проект по курсу "Базы данных" на otus

Описание:

Начало работы
### 1. Установка расширения pg_stat_statements (https://www.postgresql.org/docs/current/pgstatstatements.html)

В файле postgresql.conf добавляем расширение pg_stat_statements в shared_preload_libraries и устанавливаем доп.параметры
```
shared_preload_libraries = 'pg_stat_statements' # (change requires restart)
pg_stat_statements.track = all
compute_query_id = on
```
Перезагружаем сервер БД
```
sudo pg_ctlcluster 14 main restart
```
Создаем расширение в базе данных
```
create extension pg_stat_statements;
```

### 2. Установка pg_cron (https://github.com/citusdata/pg_cron?ysclid=lbrx7gk6g5911144098)

Устанавливаем postgresql-14-cron (для Debian)
```
sudo apt-get -y install postgresql-14-cron
```
В файле postgresql.conf добавляем расширение pg_cron в shared_preload_libraries и устанавливаем доп.параметры
```
shared_preload_libraries = 'pg_cron'
cron.database_name = 'pgstatdb'
cron.timezone = 'Europe/Moscow'
```
Создаем расширение в базе данных
```
create extension pg_cron;
```
Создаем пользователя cron_user (для создания заданий и запуска функций) и даем необходимые права
```
create user cron_user with password 'password';
grant all privileges on database pgstatdb to cron_user;
```
В файле pg_hba.conf разрешаем пользователю подключаться к БД
```
host    all             cron_user       127.0.0.1/32            trust
```
Теперь можно создавать задания для запуска функций по расписанию. 

