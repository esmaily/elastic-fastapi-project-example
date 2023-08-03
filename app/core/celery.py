from celery import Celery, Task
from celery.schedules import crontab

from kombu import Queue, Exchange

from app.core.config import settings

celery_app = Celery("fastapi-worker", broker=settings.BROKER_URL)
celery_app.conf.task_default_queue = "normal"
celery_app.conf.task_default_exchange = "normal"
celery_app.conf.default_routing_key = "normal"
celery_app.conf.task_queues = (
    Queue("high", Exchange("high", type="direct"), routing_key="high", queue_arguments={"x-max-priority": 10}),
    Queue("normal", Exchange("normal", type="direct"), routing_key="normal", queue_arguments={"x-max-priority": 5}),
    Queue("articles", Exchange("articles", type="direct"), routing_key="articles"),
)
celery_app.conf.task_routes = {
    "create_article_task": "articles",
}

celery_app.autodiscover_tasks()


class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    max_retries = 3
    retry_backoff = 300
    retry_backoff_max = 900
    retry_jitter = False
    time_limit = 60
    ignore_result = True


celery_app.conf.beat_schedule = {
    # Executes every day 0:00
    "delete_exportation": {
        "task": "save_articles_from_queue_task",
        "schedule": crontab(minute="*/1"),
    },
}
