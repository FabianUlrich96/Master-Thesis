import datetime
import googleapiclient.discovery
import pandas as pd
from googleapiclient.errors import HttpError

from database.video_list import save_video_list
import logger

log = logger.create_logger(__name__)


class YouTubeDataApi:
    def __init__(self, key, db):
        self.api_connection = None
        self.key = key
        self.db = db

    def new_connection(self):
        api_service_name = "youtube"
        api_version = "v3"

        api_connection = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=self.key)

        self.api_connection = api_connection
        log.error("test")

    def execute_search_query(self, search_query, published_before, published_after):
        page_token = ""

        try:
            while page_token is not None:
                kind = []
                result_id = []
                response = None
                try:
                    request = self.api_connection.search().list(
                        part="id", q=search_query, maxResults=50, pageToken=page_token, publishedAfter=published_after,
                        publishedBefore=published_before, fields="items()"
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
                dataframe['job'] = 1
                dataframe['page'] = 1
                now = datetime.datetime.now()
                date_now = now.strftime("%Y/%m/%d")
                dataframe['date'] = date_now
                save_video_list(self.db, dataframe)

                print(dataframe)
        except TypeError as err:
            log.error("Next page failed with error: {}".format(err))

