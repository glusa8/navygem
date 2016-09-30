from contextlib import contextmanager
from django.core.cache import cache
from gevent import sleep


@contextmanager
def lock(lock_name):
    while True:
        if cache.add(lock_name, 1):
            break
        sleep(0)
    try:
        yield
    except Exception as e:
        cache.delete(lock_name)
        raise e

    cache.delete(lock_name)
