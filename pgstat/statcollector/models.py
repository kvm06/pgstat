from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime

# pg_stat_statements snapshots
class Snapshots (models.Model):
    # snapshot created datetime
    datecr = models.DateTimeField(null=False)
    # Number of times the statement was executed
    calls = models.BigIntegerField(null=False)
    # Number of times the statement was planned( if pg_stat_statements.track_planning is enabled, otherwise zero)
    plans = models.BigIntegerField(null=False)
    # Total time spent in the statement, in milliseconds
    total_time = models.FloatField(null=False) # PG < 13, for PG >= 13 total_plan_time + total_exec_time
    # Minimum time spent in the statement, in milliseconds
    min_time = models.FloatField(null=False) # PG < 13, for PG >= 13 min_plan_time + min_exec_time
    # Maximum time spent in the statement, in milliseconds
    max_time = models.FloatField(null=False) # PG < 13, for PG >= 13 max_plan_time + max_exec_time
    # Mean time spent in the statement, in milliseconds
    mean_time = models.FloatField(null=False) # PG < 13, for PG >= 13 mean_plan_time + mean_exec_time
    # Total number of rows retrieved or affected by the statement
    rows = models.BigIntegerField(null=False)
    #Total number of shared block cache hits by the statement
    shared_blks_hit = models.BigIntegerField(null=False)
    # Total number of shared blocks read by the statement
    shared_blks_read = models.BigIntegerField(null=False)
    # Total  number of shared blocks dirtied by the statement
    shared_blks_dirtied = models.BigIntegerField(null=False)
    # Total number of shared blocks written by the statement
    shared_blks_written = models.BigIntegerField(null=False)
    #Total number of local blocks cache hits by the statement
    local_blks_hit = models.BigIntegerField(null=False)
    # Total number of local blocks read by the statement
    local_blks_read = models.BigIntegerField(null=False)
    # Total  number of local blocks dirtied by the statement
    local_blks_dirtied = models.BigIntegerField(null=False)
    # Total number of local blocks written by the statement
    local_blks_written = models.BigIntegerField(null=False)
    # Total number of temp blocks read by the statement
    temp_blks_read = models.BigIntegerField(null=False)
    # Total number of temp blocks written by the statement
    temp_blks_written = models.BigIntegerField(null=False)
    # Total time the statement spent reading blocks, in milliseconds (if track_io_timing is enabled, otherwise zero)
    blk_read_time = models.FloatField(null=False)
    # Total time the statement spent writing blocks, in milliseconds (if track_io_timing is enabled, otherwise zero)
    blk_write_time = models.FloatField(null=False)
    # Total number of WAL records generated by the statement
    wal_records = models.BigIntegerField(null=True) # PG >= 13
    # Total number of WAL full page images generated by the statement
    wal_fpi = models.BigIntegerField(null=True) # PG >= 13
    # Total amount of WAL generated by the statement in bytes
    wal_bytes = models.DecimalField(null=True, max_digits=18, decimal_places=0) # PG >= 13
    # Stats reset time from pg_stat_statements_info
    reset_time = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'QueryStat'
        verbose_name_plural = 'QueryStats'
        constraints = [
            models.UniqueConstraint(fields=['datecr'], name='datecr_unique')
        ]

class Queries (models.Model):
    # record created datetime
    datecr = models.DateTimeField(null=False)
    # OID of user who executed the statement
    userid = models.IntegerField(null=False)
    # OID of database in which the statement was executed
    dbid = models.IntegerField(null=False)
    # Hash code to identify identical normalized queries.
    queryid = models.BigIntegerField(null=False)
    # Text of a representative statement
    query = models.TextField(null=False)

    class Meta:
        verbose_name = 'Query'
        verbose_name_plural = 'Queries'
        constraints = [
            models.UniqueConstraint(fields=['dbid', 'userid','queryid'], name='dbid_userid_queryid_unique')
        ]

class Statements (models.Model):
    # statement executed datetime
    datecr = models.DateTimeField(null=False)
    # OID of user who executed the statement
    userid = models.IntegerField(null=False)
    # OID of database in which the statement was executed
    dbid = models.IntegerField(null=False)
    # Hash code to identify identical normalized queries.
    queryid = models.BigIntegerField(null=False)
    # True if the query was executed as a top - level statement(always true if pg_stat_statements.track is set to top)
    toplevel = models.BooleanField(null=True) # PG >= 14
    # Number of times the statement was executed
    calls = models.BigIntegerField(null=False)
    # Number of times the statement was planned( if pg_stat_statements.track_planning is enabled, otherwise zero)
    plans = models.BigIntegerField(null=False)
    # Total time spent in the statement, in milliseconds
    total_time = models.FloatField(null=True) # PG < 13, for PG >= 13 total_plan_time + total_exec_time
    # Minimum time spent in the statement, in milliseconds
    min_time = models.FloatField(null=True) # PG < 13, for PG >= 13 min_plan_time + min_exec_time
    # Maximum time spent in the statement, in milliseconds
    max_time = models.FloatField(null=True) # PG < 13, for PG >= 13 max_plan_time + max_exec_time
    # Mean time spent in the statement, in milliseconds
    mean_time = models.FloatField(null=True) # PG < 13, for PG >= 13 mean_plan_time + mean_exec_time
    # Total time spent planning the statement, in milliseconds( if pg_stat_statements.track_planning is enabled, otherwise zero)
    total_plan_time = models.FloatField(null=True) # PG >= 13
    # Minimum time spent planning the statement, in milliseconds (if pg_stat_statements.track_planning is enabled, otherwise zero)
    min_plan_time = models.FloatField(null=True) # PG >= 13
    # Maximum time  spent planning the statement, in milliseconds( if pg_stat_statements.track_planning is enabled, otherwise zero)
    max_plan_time = models.FloatField(null=True) # PG >= 13
    # Mean time spent planning the statement, in milliseconds( if pg_stat_statements.track_planning is enabled, otherwise zero)
    mean_plan_time = models.FloatField(null=True) # PG >= 13
    # Total time spent executing the statement, in milliseconds
    total_exec_time = models.FloatField(null=True) # PG >= 13
    # Minimum time spent executing the statement, in milliseconds
    min_exec_time = models.FloatField(null=True) # PG >= 13
    # Maximum time spent executing the statement, in milliseconds
    max_exec_time = models.FloatField(null=True) # PG >= 13
    # Mean time spent executing the statement, in milliseconds
    mean_exec_time = models.FloatField(null=True) # PG >= 13
    # Total number of rows retrieved or affected by the statement
    rows = models.BigIntegerField(null=False)
    #Total number of shared block cache hits by the statement
    shared_blks_hit = models.BigIntegerField(null=False)
    # Total number of shared blocks read by the statement
    shared_blks_read = models.BigIntegerField(null=False)
    # Total  number of shared blocks dirtied by the statement
    shared_blks_dirtied = models.BigIntegerField(null=False)
    # Total number of shared blocks written by the statement
    shared_blks_written = models.BigIntegerField(null=False)
    #Total number of local blocks cache hits by the statement
    local_blks_hit = models.BigIntegerField(null=False)
    # Total number of local blocks read by the statement
    local_blks_read = models.BigIntegerField(null=False)
    # Total  number of local blocks dirtied by the statement
    local_blks_dirtied = models.BigIntegerField(null=False)
    # Total number of local blocks written by the statement
    local_blks_written = models.BigIntegerField(null=False)
    # Total number of temp blocks read by the statement
    temp_blks_read = models.BigIntegerField(null=False)
    # Total number of temp blocks written by the statement
    temp_blks_written = models.BigIntegerField(null=False)
    # Total time the statement spent reading blocks, in milliseconds (if track_io_timing is enabled, otherwise zero)
    blk_read_time = models.FloatField(null=False)
    # Total time the statement spent writing blocks, in milliseconds (if track_io_timing is enabled, otherwise zero)
    blk_write_time = models.FloatField(null=False)
    # Total number of WAL records generated by the statement
    wal_records = models.BigIntegerField(null=True) # PG >= 13
    # Total number of WAL full page images generated by the statement
    wal_fpi = models.BigIntegerField(null=True) # PG >= 13
    # Total amount of WAL generated by the statement in bytes
    wal_bytes = models.DecimalField(null=True, max_digits=18, decimal_places=0) # PG >= 13

    class Meta:
        verbose_name = 'Statement'
        verbose_name_plural = 'Statements'

        constraints = [
            models.UniqueConstraint(fields=['datecr', 'dbid', 'userid','queryid'], name='created_dbid_userid_queryid_unique')
        ]

class Tickets(models.Model):
    ticket_no = models.CharField(primary_key=True, max_length=13)
    book_ref = models.ForeignKey('Bookings', models.DO_NOTHING, db_column='book_ref')
    passenger_id = models.CharField(max_length=20)
    passenger_name = models.TextField()
    contact_data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tickets'

class Bookings(models.Model):
    book_ref = models.CharField(primary_key=True, max_length=6)
    book_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'bookings'

class Flights(models.Model):
    flight_id = models.AutoField(primary_key=True)
    flight_no = models.CharField(max_length=6)
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    departure_airport = models.ForeignKey('AirportsData', models.DO_NOTHING, db_column='departure_airport', related_name='departure_airport')
    arrival_airport = models.ForeignKey('AirportsData', models.DO_NOTHING, db_column='arrival_airport', related_name='arrival_airport')
    status = models.CharField(max_length=20)
    aircraft_code = models.ForeignKey('AircraftsData', models.DO_NOTHING, db_column='aircraft_code')
    actual_departure = models.DateTimeField(blank=True, null=True)
    actual_arrival = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flights'
        constraints = [
            models.UniqueConstraint(fields=['flight_no', 'scheduled_departure'], name='flights_flight_no_scheduled_departure_key')
        ]

class TicketFlights(models.Model):
    ticket_no = models.OneToOneField('Tickets', models.DO_NOTHING, db_column='ticket_no', primary_key=True)
    flight_id = models.IntegerField(unique=True)
    fare_conditions = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'ticket_flights'
        # unique_together = (('ticket_no', 'flight_id'),)
        constraints = [
            models.UniqueConstraint(fields=['ticket_no', 'flight_id'], name='ticket_flights_pkey')
        ]

class Seats(models.Model):
    aircraft_code = models.OneToOneField('AircraftsData', models.DO_NOTHING, db_column='aircraft_code', primary_key=True)
    seat_no = models.CharField(max_length=4)
    fare_conditions = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'seats'
        # unique_together = (('aircraft_code', 'seat_no'),)
        constraints = [
            models.UniqueConstraint(fields=['aircraft_code', 'seat_no'], name='seats_pkey')
        ]

class AircraftsData(models.Model):
    aircraft_code = models.CharField(primary_key=True, max_length=3)
    model = models.JSONField()
    range = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'aircrafts_data'


class AirportsData(models.Model):
    airport_code = models.CharField(primary_key=True, max_length=3)
    airport_name = models.JSONField()
    city = models.JSONField()
    coordinates = models.TextField()  # This field type is a guess.
    timezone = models.TextField()

    class Meta:
        managed = False
        db_table = 'airports_data'

class BoardingPasses(models.Model):
    ticket_no = models.CharField(primary_key=True, max_length=13)
    flight = models.ForeignKey('TicketFlights', models.DO_NOTHING, to_field='flight_id')
    boarding_no = models.IntegerField()
    seat_no = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'boarding_passes'
        # unique_together = (('ticket_no', 'flight'), ('flight', 'boarding_no'), ('flight', 'seat_no'),)
        constraints = [
            models.UniqueConstraint(fields=['ticket_no', 'flight'], name='boarding_passes_pkey'),
            models.UniqueConstraint(fields=['flight', 'boarding_no'], name='boarding_passes_flight_id_boarding_no_key'),
            models.UniqueConstraint(fields=['flight', 'seat_no'], name='boarding_passes_flight_id_seat_no_key')
        ]
