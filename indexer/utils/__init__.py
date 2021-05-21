# v tem fajlju imamo fukcije za tajmer itd..

from functools import wraps
from datetime import datetime


def timing(time):
    @wraps(time)
    def wrap(*args, **kwargs):
        rezultat = time(*args, **kwargs)
        return rezultat
    return wrap


def timed(time):
    @wraps(time)
    def wrap(*args, **kwargs):
        rezultat = time(*args, **kwargs)
        starttime = datetime.now()
        mspass = ((datetime.now() - starttime).total_seconds() * 1e3)
        return mspass, rezultat
    return wrap
