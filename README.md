# pgstat
Система сбора статистики по запросам в БД PostgreSQL
Итоговый проект по курсу "Базы данных" на otus

Описание:
В БД PostgreSQL есть расширение pg_stat_statements, которое позволяет просматривать статистику
о выполненных запросах по всему кластеру БД. 
В связи с тем, что статистика собираемая данным расширением является кумулятивной, в определенных случаях,
информации недостаточно для анализа запросов. 
Данная система позволяет собирать детализованную статистику - не только за весь период, но также 
за минуту, день, неделю, месяц. 
Также система позволяет группировать запросы по базе данных, пользователю, уровню запроса (вложенный/невложенный)
Система также позволяет просматривать статистику по отдельному запросу.

Диаграмма
https://github.com/kvm06/db_course/blob/main/%D0%94%D0%B8%D0%B0%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0.png

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
grant pg_read_all_stats to cron_user;
```
В файле pg_hba.conf разрешаем пользователю подключаться к БД
```
host    all             cron_user       127.0.0.1/32            trust
```
Теперь можно создавать задания для запуска функций по расписанию. 
Основные команды:
SELECT cron.schedule('cron-задание'); 
SELECT * FROM cron.job;
SELECT * FROM cron.job_run_details
SELECT cron.unschedule(2);

### 3. Создаем процедуру save_data()
Процедура save_data сохраняет текущее состояние расширения pg_stat_statements
в таблице statcollector_last_statement. Для каждого уникального сочетания - база данных + пользователь + запрос + уровень запроса + дата сброса
статистики создается отдельная запись. Если в таблице уже есть запись с совпадающим ключем, данные
этих записей обновляются. Если записей нет, вставляются новые записи. 
Дату последнего сброса статистики получаем из расширения pg_stat_statements_info()

### 4. Создаем триггер для сохранения данных снятых за промежуток между вызовами функции
Триггер statcollector_last_statement_iud(), срабатывает при вставке/обновлении
значений в таблицу statcollector_last_statement. Он сравнивает предыдущие значения 
таблицы с новыми и сохраняет в таблицу statcollector_statement_details 
разницу между этими значениями. 

### 5. Создаем задание на ежеминутное сохранение скриншотов из pg_stat_statements
``SELECT cron.schedule(
  '* * * * *',
  $$CALL save_data();$$;
``

Данное задание будет запускаться каждую минуту и запускать процедуру save_data()
