import os


bind = "0.0.0.0:8080"
workers = 1 
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100

accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

preload_app = True
timeout = 300
keepalive = 2
graceful_timeout = 60

raw_env = [
    f"PYTHONPATH={os.getcwd()}",
    "PYTHONUNBUFFERED=1"
]


environment = os.getenv("ENVIRONMENT", "production")

if environment == "development":
    workers = 1
    reload = False
    loglevel = "debug"
    timeout = 300