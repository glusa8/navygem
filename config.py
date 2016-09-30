from multiprocessing import cpu_count


def max_workers():
    return cpu_count()

def post_fork(server, worker):
    import pymysql
    pymysql.install_as_MySQLdb()


worker_class = 'gevent'
workers = max_workers()

reload = True
