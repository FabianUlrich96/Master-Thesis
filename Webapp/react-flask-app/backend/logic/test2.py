import pause
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

api_key = 'AIzaSyDVseWOuiO1diHvWYZ0-76WM0RKEWo4DgE'


def video_comments(video_id):
    # creating youtube resource object
    youtube = build('youtube', 'v3',
                    developerKey=api_key)

    # retrieve youtube video results
    page_token = ""

    # iterate video response
    while True:
        try:
            while page_token is not None:
                response = None
                author = []
                rating = []
                likes = []
                published = []
                updated = []
                comment = []
                reply_count = []
                comment_id = []

                parent_id = []
                reply_author = []
                reply_rating = []
                reply_likes = []
                reply_published = []
                reply_updated = []
                reply_comment = []

                try:
                    request = youtube.commentThreads().list(
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
                    rating.append(item['snippet']['topLevelComment']['snippet']['viewerRating'])
                    likes.append(item['snippet']['topLevelComment']['snippet']['likeCount'])
                    published.append(item['snippet']['topLevelComment']['snippet']['publishedAt'])
                    updated.append(item['snippet']['topLevelComment']['snippet']['updatedAt'])
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
                            reply_rating.append(reply['snippet']['viewerRating'])
                            reply_likes.append(reply['snippet']['likeCount'])
                            reply_published.append(reply['snippet']['publishedAt'])
                            reply_updated.append(reply['snippet']['updatedAt'])
                            reply_comment.append(reply['snippet']['textDisplay'])

                comment_data = {'author': author, 'rating': rating, 'likes': likes, 'published': published, 'updated': updated, 'comment': comment, 'reply_count': reply_count, 'comment_id': comment_id}
                reply_data = {'parent_id': parent_id, 'author': reply_author, 'rating': reply_rating, 'likes': reply_likes, 'published': reply_published, 'updated': reply_updated, 'comment': reply_comment}

                comment_dataframe = pd.DataFrame(comment_data)
                comment_dataframe['job'] = self.job_id
                comment_dataframe['page'] = page_token
                now = datetime.now()
                date_now = now.strftime("%Y/%m/%d")
                comment_dataframe['date'] = date_now

                reply_dataframe = pd.DataFrame(reply_data)
                reply_dataframe['job'] = self.job_id
                reply_dataframe['page'] = page_token
                now = datetime.now()
                date_now = now.strftime("%Y/%m/%d")
                reply_dataframe['date'] = date_now
                YouTubeDataApi.save_comment_list(self, reply_dataframe)

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


# Enter video id
video_id = "7OtKAO8L9dE"

# Call function
video_comments(video_id)
