from django.shortcuts import render, redirect,get_object_or_404
from .models import StatementDetailsView
import json
# Create your views here.

def index(request):
    statements = StatementDetailsView.objects.filter(queryid = 7191748962367194163)
    return render(request, 'statmonitor/statlist.html', {'statements': statements})

def query(request, stat_id):
    stat = get_object_or_404(StatementDetailsView, stat_id=stat_id)
    return render(request, 'statmonitor/query.html', {'stat': stat})
