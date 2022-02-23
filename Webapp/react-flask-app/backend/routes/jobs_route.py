import datetime

from app_config import db
from flask import request, jsonify, Blueprint
from database.models import Jobs, VideoList
from database.schemas import JobsSchema
from database.models import Apis
from database.models import CommentList
from database.models import ReplyList
from logic.YouTubeDataApi import YouTubeDataApi
from logic.GoogleTranslate import GoogleTranslate

import logger
import pandas as pd
from sqlalchemy.exc import IntegrityError

log = logger.create_logger(__name__)
job_schema = JobsSchema()
jobs_schema = JobsSchema(many=True)
jobs_blueprint = Blueprint('jobs_blueprint', __name__, template_folder='templates')


@jobs_blueprint.route('/jobs', methods=['GET', 'POST', 'DELETE'])
def jobs_all():
    if request.method == 'GET':
        jobs = db.session.query(Jobs).all()
        return jsonify(jobs_schema.dump(jobs))

    if request.method == 'POST':
        all_data = request.json
        job_type = all_data["job_type"]

        log.info(all_data)
        selected_job = None
        name = None
        api = None
        query = None
        published_before = None
        published_after = None

        if "selected_job" in all_data:
            selected_job = all_data["selected_job"]
        if "name" in all_data:
            name = all_data["name"]
        date = datetime.datetime.now()
        if "query" in all_data:
            query = all_data["query"]
        if "published_before" in all_data:
            published_before = all_data["published_before"]
        if "published_after" in all_data:
            published_after = all_data["published_after"]
        done = False
        failed = False

        if "api" in all_data:
            api = all_data["api"]
            api_row = db.session.query(Apis).filter(Apis.name == api).first()
            key = api_row.token

        job_id = ""
        try:
            job = Jobs(None, job_type, api, name, date, query, done, published_before, published_after, failed)
            db.session.add(job)
            db.session.flush()
            db.session.refresh(job)
            job_id = job.job_id
            db.session.commit()
        except IntegrityError as e:
            log.error(e)

        if job_type == "comment":
            job = YouTubeDataApi(job_id, key, db)
            YouTubeDataApi.new_connection(job)
            videos = db.session.query(VideoList.video_id).filter(VideoList.job == selected_job).all()

            video_ids = [item[0] for item in videos]

            for video in video_ids:
                YouTubeDataApi.get_comments(job, video)

        if job_type == "video":
            job = YouTubeDataApi(job_id, key, db)
            YouTubeDataApi.new_connection(job)
            YouTubeDataApi.execute_search_query(job, query, published_before, published_after)

        if job_type == "video_loader":
            file = all_data['file']

            video_df = pd.DataFrame(file)
            new_header = video_df.iloc[0]
            video_df = video_df[1:]
            video_df.columns = new_header
            video_df = video_df.drop('id', axis=1)
            video_df = video_df.drop('job', axis=1)
            video_df['job'] = job_id
            try:
                video_df.to_sql('video_list', con=db.engine, if_exists='append', chunksize=1000, index=False)
            except IntegrityError as e:
                log.error(e)

        if job_type == "translation":
            job = GoogleTranslate(job_id, db)
            execute = True
            limit = 1000
            offset = 0
            while execute:

                comments = db.session.query(CommentList.comment).filter(
                    CommentList.translation == None, CommentList.job == selected_job).limit(limit).offset(offset).all()
                log.info(comments)
                if not comments:
                    execute = False
                else:
                    offset = offset + 1000
                    raw_comments = [item[0] for item in comments]
                    log.info(raw_comments)
                    GoogleTranslate.translate_text(job, raw_comments, "comment_list")

            execute = True
            limit = 1000
            offset = 0
            while execute:

                comments = db.session.query(ReplyList.comment).filter(
                    ReplyList.translation == None, ReplyList.job == selected_job).limit(limit).offset(offset).all()
                if not comments:
                    execute = False
                else:
                    offset = offset + 1000
                    raw_comments = [item[0] for item in comments]
                    log.info(raw_comments)
                    GoogleTranslate.translate_text(job, raw_comments, "reply_list")


        return 'Ok'
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')


@jobs_blueprint.route('/jobs/<job_id>', methods=['GET', 'POST', 'DELETE'])
def jobs_id(job_id):
    if request.method == 'GET':
        return job_id
    if request.method == 'POST':
        print('post things')
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')
