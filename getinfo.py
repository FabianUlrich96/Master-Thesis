import googleapiclient.discovery
import pandas as pd


def getinfo():
    video_info = {
        'id': [],
        'duration': [],
        'views': [],
        'likes': [],
        'dislikes': [],
        'favorites': [],
        'comments': []
    }

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyDVseWOuiO1diHvWYZ0-76WM0RKEWo4DgE"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.search().list(
        part="id", q="e-auto", maxResults=50, fields="items(id(videoId))"
    )
    # Query execution
    response = request.execute()
    # Print the results
    print(response)

    for item in response['items']:

        vidId = item['id']['videoId']
        r = youtube.videos().list(
            part="statistics,contentDetails",
            id=vidId,
            fields="items(statistics," + \
                   "contentDetails(duration))"
        ).execute()

        try:
            duration = r['items'][0]['contentDetails']['duration']
            views = r['items'][0]['statistics']['viewCount']
            likes = r['items'][0]['statistics']['likeCount']
            dislikes = r['items'][0]['statistics']['dislikeCount']
            favorites = r['items'][0]['statistics']['favoriteCount']
            comments = r['items'][0]['statistics']['commentCount']
            video_info['id'].append(vidId)
            video_info['duration'].append(duration)
            video_info['views'].append(views)
            video_info['likes'].append(likes)
            video_info['dislikes'].append(dislikes)
            video_info['favorites'].append(favorites)
            video_info['comments'].append(comments)
        except:
            pass

        pd.DataFrame(data=video_info).to_csv("video.csv", index=False)


def main():
    getinfo()


if __name__ == '__main__':
    main()
