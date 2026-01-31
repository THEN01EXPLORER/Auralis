import os
from celery import Celery

# Use environment variable directly here or import settings carefully to avoid circular imports 
# if settings imports something that imports this.
# Ideally use settings.
from app.core.config import settings

celery_app = Celery("job_queue", broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"))

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    worker_concurrency=int(os.getenv("WORKER_CONCURRENCY", 4)),
    task_time_limit=300, # 5 min hard limit
    task_soft_time_limit=240, # 4 min soft limit
)
