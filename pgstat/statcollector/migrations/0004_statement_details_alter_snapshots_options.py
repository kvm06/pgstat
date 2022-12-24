# Generated by Django 4.1.4 on 2022-12-18 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statcollector', '0003_aircraftsdata_airportsdata_boardingpasses_flights_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statement_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datecr', models.DateTimeField()),
                ('userid', models.IntegerField()),
                ('dbid', models.IntegerField()),
                ('queryid', models.BigIntegerField()),
                ('toplevel', models.BooleanField(null=True)),
                ('calls', models.BigIntegerField()),
                ('plans', models.BigIntegerField()),
                ('total_time', models.FloatField(null=True)),
                ('min_time', models.FloatField(null=True)),
                ('max_time', models.FloatField(null=True)),
                ('mean_time', models.FloatField(null=True)),
                ('total_plan_time', models.FloatField(null=True)),
                ('min_plan_time', models.FloatField(null=True)),
                ('max_plan_time', models.FloatField(null=True)),
                ('mean_plan_time', models.FloatField(null=True)),
                ('total_exec_time', models.FloatField(null=True)),
                ('min_exec_time', models.FloatField(null=True)),
                ('max_exec_time', models.FloatField(null=True)),
                ('mean_exec_time', models.FloatField(null=True)),
                ('rows', models.BigIntegerField()),
                ('shared_blks_hit', models.BigIntegerField()),
                ('shared_blks_read', models.BigIntegerField()),
                ('shared_blks_dirtied', models.BigIntegerField()),
                ('shared_blks_written', models.BigIntegerField()),
                ('local_blks_hit', models.BigIntegerField()),
                ('local_blks_read', models.BigIntegerField()),
                ('local_blks_dirtied', models.BigIntegerField()),
                ('local_blks_written', models.BigIntegerField()),
                ('temp_blks_read', models.BigIntegerField()),
                ('temp_blks_written', models.BigIntegerField()),
                ('blk_read_time', models.FloatField()),
                ('blk_write_time', models.FloatField()),
                ('wal_records', models.BigIntegerField(null=True)),
                ('wal_fpi', models.BigIntegerField(null=True)),
                ('wal_bytes', models.DecimalField(decimal_places=0, max_digits=18, null=True)),
            ],
            options={
                'verbose_name': 'Statement_detail',
                'verbose_name_plural': 'Statements_details',
            },
        ),
        migrations.AlterModelOptions(
            name='snapshots',
            options={'verbose_name': 'Statement', 'verbose_name_plural': 'Statements'},
        ),
    ]