from django import template
from math import floor

register = template.Library()

def pretty_size(bytes):
    power = 2 ** 10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while bytes > power:
        bytes /= power
        n += 1
    return "%s %s" % (floor(bytes), power_labels[n] + ('bytes' if n == 0 else 'B'))

def query_date(date):
    print(date)

register.filter('pretty_size', pretty_size)
