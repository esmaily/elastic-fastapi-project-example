from app.core.celery import celery_app, BaseTaskWithRetry


@celery_app.task(name="create_article_task", base=BaseTaskWithRetry)
def create_article_task(article) -> str:
    return f"article store in broker {article}"


@celery_app.task(name="save_articles_from_queue_task", base=BaseTaskWithRetry)
def save_articles_from_queue_task() -> str:
    article=""
    print("tes")
    return f"article store in broker {article}"