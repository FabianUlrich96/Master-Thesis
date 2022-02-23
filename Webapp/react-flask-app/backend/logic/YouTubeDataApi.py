import datetime
import googleapiclient.discovery
from sqlalchemy.exc import IntegrityError
import pandas as pd
from googleapiclient.errors import HttpError
import pause
from datetime import datetime
import logger

log = logger.create_logger(__name__)


class YouTubeDataApi(object):
    def __init__(self, job_id, key, db):
        self.api_connection = None
        self.job_id = job_id
        self.key = key
        self.db = db

    def save_video_list(self, data):
        try:
            data.to_sql('video_list', con=self.db.engine, if_exists='append', chunksize=1000, index=False)
        except IntegrityError as e:
            log.error(e)

    def new_connection(self):
        api_service_name = "youtube"
        api_version = "v3"

        api_connection = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=self.key)

        self.api_connection = api_connection

    def execute_search_query(self, search_query, published_before, published_after):
        page_token = ""
        before_object = datetime.strptime(published_before, '%Y-%m-%d')
        after_object = datetime.strptime(published_after, '%Y-%m-%d')
        before = before_object.isoformat("T") + "Z"
        after = after_object.isoformat("T") + "Z"
        while True:
            try:
                while page_token is not None:
                    kind = []
                    result_id = []
                    response = None
                    try:
                        request = self.api_connection.search().list(
                            part="id", q=search_query, maxResults=50, pageToken=page_token, publishedAfter=after,
                            publishedBefore=before, fields="items()"
                        )
                        response = request.execute()

                    except HttpError as err:
                        log.error("HTTP Error: {}".format(err))

                    try:
                        page_token = response["nextPageToken"]
                    except KeyError:
                        page_token = None

                    for item in response["items"]:
                        kind.append(item["kind"])
                        try:
                            result_id.append(item["id"]["videoId"])

                        except KeyError:
                            try:
                                result_id.append(item["id"]["channelId"])
                            except KeyError:
                                result_id.append(None)
                    data = {'kind': kind, 'video_id': result_id}
                # Save each badge to database
                    dataframe = pd.DataFrame(data)
                    dataframe['job'] = self.job_id
                    dataframe['page'] = page_token
                    now = datetime.now()
                    date_now = now.strftime("%Y/%m/%d")
                    dataframe['date'] = date_now
                    dataframe['translation'] = None
                    YouTubeDataApi.save_video_list(self, dataframe)

                    print(dataframe)
            except TypeError as err:
                log.error("Next page failed with error: {}".format(err))
            except HttpError as err:
                log.error("Execution failed with error: {]".format(err))
                log.info("")
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                time_eod = '00:00:00'
                time_format = '%H:%M:%S'
                time_delta = datetime.strptime(current_time, time_format) - datetime.strptime(time_eod, time_format)
                log.info("Idling for {} seconds".format(time_delta.seconds))
                pause.seconds(time_delta.seconds)
                continue

            break

    def save_reply_list(self, data):
        try:
            data.to_sql('reply_list', con=self.db.engine, if_exists='append', chunksize=1000, index=False)
        except IntegrityError as e:
            log.error(e)

    def save_comment_list(self, data):
        try:
            data.to_sql('comment_list', con=self.db.engine, if_exists='append', chunksize=1000, index=False)
        except IntegrityError as e:
            log.error(e)

    def get_comments(self, video_id):
        page_token = ""

        while True:
            try:
                while page_token is not None:
                    response = None
                    author = []
                    likes = []
                    published = []
                    updated = []
                    comment = []
                    reply_count = []
                    comment_id = []

                    parent_id = []
                    reply_author = []
                    reply_likes = []
                    reply_published = []
                    reply_updated = []
                    reply_comment = []

                    try:
                        request = self.api_connection.commentThreads().list(
                            maxResults=50,
                            part='snippet,replies',
                            videoId=video_id,
                            pageToken=page_token
                        )
                        response = request.execute()
                    except HttpError as err:
                        print(err)
                    # log.error("HTTP Error: {}".format(err))
                    try:
                        page_token = response["nextPageToken"]
                    except KeyError:
                        page_token = None

                    print(response)

                    for item in response['items']:
                        author.append(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                        likes.append(item['snippet']['topLevelComment']['snippet']['likeCount'])
                        published_string = item['snippet']['topLevelComment']['snippet']['publishedAt'][:-1]
                        published_date = datetime.fromisoformat(published_string)
                        published.append(published_date)

                        updated_string = item['snippet']['topLevelComment']['snippet']['updatedAt'][:-1]
                        updated_date = datetime.fromisoformat(updated_string)
                        updated.append(updated_date)

                        comment.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                        reply_count.append(item['snippet']['totalReplyCount'])
                        comment_id.append(item['snippet']['topLevelComment']['id'])

                        replies = item['snippet']['totalReplyCount']

                        # if reply is there
                        if replies > 0:

                            # iterate through all reply
                            for reply in item['replies']['comments']:
                                # Extract reply
                                parent_id.append(reply['snippet']['parentId'])
                                reply_author.append(reply['snippet']['authorDisplayName'])
                                reply_likes.append(reply['snippet']['likeCount'])

                                reply_published_string = reply['snippet']['publishedAt'][:-1]
                                reply_published_date = datetime.fromisoformat(reply_published_string)
                                reply_published.append(reply_published_date)
                                reply_updated_string = reply['snippet']['updatedAt'][:-1]
                                reply_updated_date = datetime.fromisoformat(reply_updated_string)
                                reply_updated.append(reply_updated_date)

                                reply_comment.append(reply['snippet']['textDisplay'])

                    comment_data = {'video_id': video_id, 'author': author, 'likes': likes, 'published': published,
                                    'updated': updated, 'comment': comment, 'reply_count': reply_count,
                                    'comment_id': comment_id}
                    reply_data = {'video_id': video_id, 'parent_id': parent_id, 'author': reply_author, 'likes': reply_likes, 'published': reply_published, 'updated': reply_updated,
                                  'comment': reply_comment}

                    comment_dataframe = pd.DataFrame(comment_data)
                    comment_dataframe['job'] = self.job_id
                    comment_dataframe['page'] = page_token
                    now = datetime.now()
                    date_now = now.strftime("%Y/%m/%d")
                    comment_dataframe['date'] = date_now
                    YouTubeDataApi.save_comment_list(self, comment_dataframe)

                    reply_dataframe = pd.DataFrame(reply_data)
                    reply_dataframe['job'] = self.job_id
                    reply_dataframe['page'] = page_token
                    now = datetime.now()
                    date_now = now.strftime("%Y/%m/%d")
                    reply_dataframe['date'] = date_now

                    YouTubeDataApi.save_reply_list(self, reply_dataframe)

            except TypeError as err:
                log.error("Next page failed with error: {}".format(err))
            except HttpError as err:
                log.error("Execution failed with error: {]".format(err))
                log.info("")
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                time_eod = '00:00:00'
                time_format = '%H:%M:%S'
                time_delta = datetime.strptime(current_time, time_format) - datetime.strptime(time_eod, time_format)
                log.info("Idling for {} seconds".format(time_delta.seconds))
                pause.seconds(time_delta.seconds)
                continue

            break
