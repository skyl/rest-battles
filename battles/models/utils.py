import datetime
from battles.models.constants import DATE_FORMAT_STR


def deserialize_dt(s):
    return datetime.datetime.strptime(s, DATE_FORMAT_STR)


def serialize_dt(d):
    return d.strftime(DATE_FORMAT_STR)
