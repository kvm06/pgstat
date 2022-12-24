# Generated by Django 4.1.4 on 2022-12-18 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statcollector', '0004_statement_details_alter_snapshots_options'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='statements',
            name='created_dbid_userid_queryid_unique',
        ),
        migrations.AddConstraint(
            model_name='statements',
            constraint=models.UniqueConstraint(fields=('dbid', 'userid', 'queryid', 'toplevel'), name='dbid_userid_queryid_toplevel_unique'),
        ),
    ]