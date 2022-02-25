from sqlalchemy.orm import sessionmaker
import logger
from celery import Celery
from celery.utils.log import get_task_logger
from logic.YouTubeDataApi import execute_search_query
from logic.YouTubeDataApi import get_comments
from logic.GoogleTranslate import translate_text
from sqlalchemy import create_engine
from database.models import CommentList
from database.models import ReplyList


log = logger.create_logger(__name__)

celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

engine = create_engine('mysql+pymysql://dataapi:fnmwm4d833834erjn@dataapidb/dataapi?charset=utf8mb4')
Session = sessionmaker(bind=engine)
session = Session()


@celery.task(queue="video")
def query_videos(key, job_id, query, published_before, published_after):
    execute_search_query(key, job_id, query, published_before, published_after)


@celery.task(queue="comments")
def query_comments(key, job_id, video_ids):
    for video in video_ids:
        get_comments(key, job_id, video)


@celery.task(queue="translation")
def translate_comments(selected_job):
    execute = True
    limit = 1000
    offset = 0
    while execute:

        comments = session.query(CommentList.comment).filter(
            CommentList.translation == None, CommentList.job == selected_job).limit(limit).offset(offset).all()
        if not comments:
            execute = False
        else:
            offset = offset + 1000
            raw_comments = [item[0] for item in comments]
            translate_text(raw_comments, "comment_list")


@celery.task(queue="translation")
def translate_replies(selected_job):
    execute = True
    limit = 1000
    offset = 0
    while execute:

        comments = session.query(ReplyList.comment).filter(
            ReplyList.translation == None, ReplyList.job == selected_job).limit(limit).offset(offset).all()
        if not comments:
            execute = False
        else:
            offset = offset + 1000
            raw_comments = [item[0] for item in comments]
            log.info(raw_comments)
            translate_text(raw_comments, "reply_list")


