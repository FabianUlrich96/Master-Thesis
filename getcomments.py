import googleapiclient.discovery
import pandas as pd


# data api https://medium.com/mcd-unison/youtube-data-api-v3-in-python-tutorial-with-examples-e829a25d2ebd#f8ef
# Comment thread limitation: https://stackoverflow.com/questions/29974742/youtube-data-api-v3-comment-thread-discrepency
# rate limit 10.000 requests per day per API key --> 12 projects with keys possible for each account


def get_threads(comments, youtube):
    threads = []
    video_id = "sOESZIQz-lA"
    page_token = ""

    while page_token is not None:
        request = youtube.commentThreads().list(
            part="snippet", videoId=video_id, textFormat="plainText", maxResults=100, pageToken=page_token
        )

        response = request.execute()

        for item in response["items"]:
            threads.append(item["id"])
            comment = item["snippet"]["topLevelComment"]
            text = comment["snippet"]["textDisplay"]
            comments.append(text)
        try:
            page_token = response["nextPageToken"]
        except:
            page_token = None

            return threads


def get_comments(parent_id, comments, youtube):
    print(len(parent_id))

    for i in parent_id:
        print(i)
        results = youtube.comments().list(
            part="snippet",
            parentId=i,
            textFormat="plainText",
            maxResults=100
        ).execute()
        for item in results["items"]:
            # likeCount , publishedAt, updatedAt, authorChannelId under item["snippet"]["value"]
            print(item["snippet"])
            text = item["snippet"]["textDisplay"]
            comments.append(text)


def main():
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyDVseWOuiO1diHvWYZ0-76WM0RKEWo4DgE"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    comments = []
    thread = get_threads(comments, youtube)
    get_comments(thread, comments, youtube)

    pd.DataFrame(data=comments).to_csv("comments.csv", index=False)
    print(len(comments))


if __name__ == '__main__':
    main()
