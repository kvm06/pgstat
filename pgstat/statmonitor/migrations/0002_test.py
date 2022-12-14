# Generated by Django 4.1.4 on 2022-12-21 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statmonitor', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP VIEW statement_details_view;
            CREATE OR REPLACE VIEW statement_details_view AS
            SELECT 
                a.id as stat_id,
                a.queryid,
                a.userid,
                a.dbid,
                a.datecr,
                a.calls,
                a.plans,
                a.total_exec_time / 1000::double precision AS exec_time,
                a.total_plan_time / 1000::double precision AS plan_time,
                a.total_exec_time / 1000::double precision / NULLIF(a.calls, 0)::double precision AS exec_time_per_query,
                a.total_plan_time / 1000::double precision / NULLIF(a.plans, 0)::double precision AS plan_time_per_plan,
                a.rows AS total_rows,
                a.rows / NULLIF(a.calls, 0) AS rows_per_query,
                pg_size_pretty(a.shared_blks_hit::numeric * 8192::numeric) AS cache_hit,
                pg_size_pretty(a.shared_blks_read::numeric * 8192::numeric) AS cache_miss,
                pg_size_pretty(a.shared_blks_hit / NULLIF(a.calls, 0) * 8192) AS cache_hit_per_query,
                pg_size_pretty(a.shared_blks_read / NULLIF(a.calls, 0) * 8192) AS cache_miss_per_query,
                100.0 * a.shared_blks_hit::numeric / NULLIF(a.shared_blks_hit + a.shared_blks_read, 0)::numeric AS hit_percent,
                pg_size_pretty(a.temp_blks_written::numeric * 8192::numeric) AS temp_bytes,
                pg_size_pretty(a.temp_blks_written / NULLIF(a.calls, 0) * 8192) AS temp_bytes_written_per_query,
                a.wal_bytes,
                a.wal_bytes / NULLIF(a.calls, 0)::numeric AS wal_bytes_per_query
               FROM statcollector_statement_details as a;
            """
        ),
    ]
