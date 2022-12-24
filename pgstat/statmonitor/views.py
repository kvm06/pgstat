from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Sum, Case, When
from django.db.models.functions.comparison import NullIf, Coalesce
from django.contrib.postgres.aggregates import StringAgg
from .models import StatementDetailsView,  PERIOD_CHOICES
from statcollector.models import Queries

from .forms import FilterForm
import json
# Create your views here.
from django.db import connection

def index(request):
    # statements = StatementDetailsView.objects.filter(queryid=7191748962367194163)
    statements = StatementDetailsView.objects.all()

    if len(request.GET):
        filter_form = FilterForm(request.GET)
    else:
        filter_form = FilterForm({'group_dbs': True,
                                  'group_users': True,
                                  'group_levels': True,
                                  'period': 'minute'})

    groupping_columns = []

    if filter_form.is_valid():
        group_dbs = filter_form.cleaned_data['group_dbs']
        if not group_dbs:
            groupping_columns.append('datname')

        group_users = filter_form.cleaned_data['group_users']
        if not group_users:
            groupping_columns.append('rolname')

        group_levels = filter_form.cleaned_data['group_levels']
        if not group_levels:
            groupping_columns.append('toplevel')

        period = filter_form.cleaned_data['period']

        if period == 'minute':
            groupping_columns.append('query_minute')
        elif period == 'hour':
            groupping_columns.append('query_hour')
        elif period == 'day':
            groupping_columns.append('query_day')
        elif period == 'week':
            groupping_columns.append('query_week')
        elif period == 'month':
            groupping_columns.append('query_month')

        if groupping_columns:
            groupping_columns.append('queryid')
            print(groupping_columns)
            statements = statements.values(*groupping_columns).annotate(
                rolname_aggr=StringAgg('rolname', delimiter=", ", distinct=True),
                datname_aggr=StringAgg('datname', delimiter=", ", distinct=True),
                calls=Sum('calls'),
                plans=Sum('plans'),
                rows=Sum('rows'),
                total_exec_time=Sum('total_exec_time'),
                shared_blks_read_size=Sum('shared_blks_read_size'),
                local_blks_read_size=Sum('local_blks_read_size'),
                temp_blks_read_size=Sum('temp_blks_read_size'),
                shared_blks_written_size=Sum('shared_blks_written_size'),
                local_blks_written_size=Sum('local_blks_written_size'),
                temp_bytes_written_size=Sum('temp_bytes_written_size'),
                shared_blks_hit_percent=100 * Sum('shared_blks_hit_size') / NullIf(Sum('shared_blks_hit_size') + Sum('shared_blks_read'), 0),
                local_blks_hit_percent=100 * Sum('local_blks_hit_size') / NullIf(Sum('local_blks_hit_size') + Sum('local_blks_read'), 0)
            )
    else:
        filter_form = FilterForm()

    return render(request, 'statmonitor/index.html', {'statements': statements, 'filter_form': filter_form})

def query(request, queryid):
    statements = StatementDetailsView.objects.filter(queryid=queryid)
    query_text = Queries.objects.filter(queryid=queryid).first().query

    if len(request.GET):
        filter_form = FilterForm(request.GET)
    else:
        filter_form = FilterForm({'group_dbs': True,
                                  'group_users': True,
                                  'group_levels': True,
                                  'period': 'minute'})

    groupping_columns = []

    if filter_form.is_valid():
        group_dbs = filter_form.cleaned_data['group_dbs']
        if not group_dbs:
            groupping_columns.append('datname')

        group_users = filter_form.cleaned_data['group_users']
        if not group_users:
            groupping_columns.append('rolname')

        group_levels = filter_form.cleaned_data['group_levels']
        if not group_levels:
            groupping_columns.append('toplevel')

        period = filter_form.cleaned_data['period']

        if period == 'minute':
            groupping_columns.append('query_minute')
        elif period == 'hour':
            groupping_columns.append('query_hour')
        elif period == 'day':
            groupping_columns.append('query_day')
        elif period == 'week':
            groupping_columns.append('query_week')
        elif period == 'month':
            groupping_columns.append('query_month')

        if groupping_columns:
            groupping_columns.append('queryid')
            print(groupping_columns)
            statements = statements.values(*groupping_columns).annotate(
                rolname_aggr=StringAgg('rolname', delimiter=", ", distinct=True),
                datname_aggr=StringAgg('datname', delimiter=", ", distinct=True),
                calls=Sum('calls'),
                plans=Sum('plans'),
                rows=Sum('rows'),
                total_exec_time=Sum('total_exec_time'),
                shared_blks_read_size=Sum('shared_blks_read_size'),
                local_blks_read_size=Sum('local_blks_read_size'),
                temp_blks_read_size=Sum('temp_blks_read_size'),
                shared_blks_written_size=Sum('shared_blks_written_size'),
                local_blks_written_size=Sum('local_blks_written_size'),
                temp_bytes_written_size=Sum('temp_bytes_written_size'),
                shared_blks_hit_percent=100 * Sum('shared_blks_hit_size') / NullIf(Sum('shared_blks_hit_size') + Sum('shared_blks_read'), 0),
                local_blks_hit_percent=100 * Sum('local_blks_hit_size') / NullIf(Sum('local_blks_hit_size') + Sum('local_blks_read'), 0)
            )
    else:
        filter_form = FilterForm()

    return render(request, 'statmonitor/query.html', {'statements': statements, 'filter_form': filter_form, 'query_text':query_text})
