from django.db import models
from django.db.models import Aggregate
from django.forms import CharField

PERIOD_CHOICES = (
        ('minute', 'минута'),
        ('hour', 'час'),
        ('day', 'день'),
        ('week', 'неделя'),
        ('month', 'месяц')
    )

class StatementDetailsView (models.Model):
    stat_id = models.IntegerField(primary_key=True)
    datecr = models.DateTimeField(null=False)
    query_minute = models.DateTimeField(null=False)
    query_hour = models.DateTimeField(null=False)
    query_day = models.DateTimeField(null=False)
    query_week= models.DateTimeField(null=False)
    query_month = models.DateTimeField(null=False)
    rolname = models.TextField()
    datname = models.TextField()
    toplevel = models.BooleanField(null=False)
    queryid = models.BigIntegerField(null=False)
    calls = models.BigIntegerField(null=False)
    plans = models.BigIntegerField(null=False)
    rows = models.BigIntegerField(null=False)
    total_plan_time = models.FloatField(null=False)
    total_exec_time = models.FloatField(null=False)
    shared_blks_read_size = models.BigIntegerField(null=False)
    local_blks_read_size = models.BigIntegerField(null=False)
    temp_blks_read_size = models.BigIntegerField(null=False)
    shared_blks_written_size = models.BigIntegerField(null=False)
    temp_bytes_written_size = models.BigIntegerField(null=False)
    local_blks_written_size = models.BigIntegerField(null=False)
    shared_blks_hit_size = models.BigIntegerField(null=False)
    local_blks_hit_size = models.BigIntegerField(null=False)
    shared_blks_hit_percent = models.TextField()
    local_blks_hit_percent = models.TextField()
    shared_blks_read = models.BigIntegerField(null=False)
    local_blks_read = models.BigIntegerField(null=False)

    class Meta:
        managed = False
        db_table='statement_details_view'

