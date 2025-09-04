"""
Celery application configuration.
"""

from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "pm_ai_backend",
    broker=getattr(settings, 'CELERY_BROKER_URL', 'redis://localhost:6379/1'),
    backend=getattr(settings, 'CELERY_RESULT_BACKEND', 'redis://localhost:6379/1'),
    include=[
        'app.tasks.import_tasks',
        'app.tasks.report_tasks',
        'app.tasks.ai_tasks'
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)
