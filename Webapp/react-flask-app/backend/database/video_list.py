from sqlalchemy.exc import IntegrityError
import logger


def save_video_list(db, data):
    log = logger.create_logger(__name__)

    try:
        data.to_sql('Video_List', con=db.engine, if_exists='append', chunksize=1000, index=False)
    except IntegrityError as e:
        log.error(e)
