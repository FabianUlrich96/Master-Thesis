from celery import Celery
from celery.utils.log import get_task_logger
from YouTubeDataApi import execute_search_query
from YouTubeDataApi import get_comments
#from GoogleTranslate import translate_text
from sqlalchemy import create_engine
#from database.models import CommentList

logger = get_task_logger(__name__)

celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
db = create_engine('mysql+pymysql://dataapi:fnmwm4d833834erjn@dataapidb/dataapi?charset=utf8mb4')


@celery.task(queue="video")
def query_videos(key, job_id, query, published_before, published_after):
    execute_search_query(key, job_id, query, published_before, published_after)


@celery.task(queue="comments")
def query_comments(key, job_id, video_ids):
    for video in video_ids:
        get_comments(key, job_id, video)


@celery.task(queue="translation")
def translate_comments(job, selected_job):
    execute = True
    limit = 1000
    offset = 0
    while execute:

        comments = db.session.query(CommentList.comment).filter(
            CommentList.translation == None, CommentList.job == selected_job).limit(limit).offset(offset).all()
        if not comments:
            execute = False
        else:
            offset = offset + 1000
            raw_comments = [item[0] for item in comments]
            #translate_text(raw_comments, "comment_list")

