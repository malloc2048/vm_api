import os
from distutils.util import strtobool

DEFAULT_GUNICORN_HOST = "0.0.0.0"
DEFAULT_GUNICORN_PORT = 8001

bind_host = os.environ.get("GUNICORN_HOST", DEFAULT_GUNICORN_HOST)
bind_port = os.environ.get("GUNICORN_PORT", DEFAULT_GUNICORN_PORT)
bind = f"{bind_host}:{bind_port}"

DEFAULT_GUNICORN_WORKER_COUNT = 4
configured_workers = os.environ.get("GUNICORN_WORKER_COUNT", DEFAULT_GUNICORN_WORKER_COUNT)

reload = True

accesslog = "-"
access_log_format = '%(t)s %(h)s "%(r)s" %(s)s "%(a)s"'

chdir = "/home/app/api"
