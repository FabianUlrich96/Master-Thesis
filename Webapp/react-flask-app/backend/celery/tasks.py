import time
from celery import Celery
from celery.utils.log import get_task_logger
from YouTubeDataApi import execute_search_query

logger = get_task_logger(__name__)

celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@celery.task()
def longtime_add(x, y):
    logger.info('Got Request - Starting work ')
    time.sleep(4)
    logger.info('Work Finished ')
    return x + y


@celery.task()
def query_videos(key, job_id, query, published_before, published_after):
    execute_search_query(key, job_id, query, published_before, published_after)
