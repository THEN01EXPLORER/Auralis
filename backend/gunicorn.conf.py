# Gunicorn configuration for production deployment
import os
import multiprocessing

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"
backlog = 2048

# Worker processes - REDUCED for Render free tier (512MB RAM limit)
# Default to 2 workers to stay under memory limit (~200MB per worker)
workers = int(os.getenv('WORKERS', '2'))
worker_class = 'uvicorn.workers.UvicornWorker'
worker_connections = 1000
timeout = 300  # 5 minutes for long-running analysis
keepalive = 5

# Memory optimization
preload_app = True  # Share memory across workers
max_requests = 1000  # Restart workers periodically to prevent memory leaks
max_requests_jitter = 50

# Logging
accesslog = '-'
errorlog = '-'
loglevel = os.getenv('LOG_LEVEL', 'info').lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'auralis-api'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
# keyfile = None
# certfile = None
