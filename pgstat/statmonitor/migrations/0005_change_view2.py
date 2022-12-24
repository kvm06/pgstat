# Generated by Django 4.1.4 on 2022-12-21 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statmonitor', '0004_change_view'),
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP VIEW statement_details_view;
            CREATE OR REPLACE VIEW statement_details_view AS
            SELECT 
                a.id AS stat_id,
                a.queryid,
                pg_roles.rolname,
                pg_database.datname,
                to_char(a.datecr, 'dd.mm.yyyy hh24:mi:ss') as datecr,
                a.calls,
                a.plans,
                a.rows,
                to_char(a.total_exec_time / 1000::double precision, 'FM9999999990D099') AS total_exec_time,
                to_char(a.total_plan_time / 1000::double precision, 'FM9999999990D099') AS total_plan_time,
                pg_size_pretty(a.shared_blks_read::numeric * 8192::numeric) AS shared_blks_read_size,
                pg_size_pretty(a.local_blks_read::numeric * 8192::numeric) AS local_blks_read_size,
                pg_size_pretty(a.temp_blks_read::numeric * 8192::numeric) AS temp_blks_read_size,
                pg_size_pretty(a.shared_blks_written::numeric * 8192::numeric) AS shared_blks_written_size,
                pg_size_pretty(a.temp_blks_written::numeric * 8192::numeric) AS temp_bytes_written_size,
                pg_size_pretty(a.local_blks_written::numeric * 8192::numeric) AS local_blks_written_size,
                coalesce(to_char(100.0 * a.shared_blks_hit::numeric / NULLIF(a.shared_blks_hit + a.shared_blks_read, 0)::numeric, 'FM9999999990D09'), ' - ') AS shared_blks_hit_percent,
                coalesce(to_char(100.0 * a.local_blks_hit::numeric / NULLIF(a.local_blks_hit + a.local_blks_read, 0)::numeric, 'FM9999999990D09'), ' - ') AS local_blks_hit_percent
            FROM statcollector_statement_details a
            INNER JOIN pg_roles on a.userid=pg_roles.oid
            INNER JOIN pg_database on a.dbid=pg_database.oid;
            """
        ),
    ]