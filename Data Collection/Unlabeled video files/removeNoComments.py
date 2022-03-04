import pandas as pd
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from langdetect import detect


def load_dataframe():
    filename = input("File name in folder: ")
    filename = f'{filename}.csv'
    csv_file = pd.read_csv(filename)

    return csv_file, filename


def save_dataframe(result_df, filename):
    result_df["job"] = 0
    result_df["id"] = 0
    size = len(filename)
    filename = filename[:size - 4]
    new_filename = f'{filename}_with_information.csv'
    try:
        result_df.to_csv(new_filename, mode='a', index=False)
    except:
        result_df.to_csv("in_save_mode.csv")


def new_connection(key):
    api_service_name = "youtube"
    api_version = "v3"

    api_connection = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=key)

    return api_connection


def load_information(key, videos, filename):
    page_token = ""

    while page_token is not None:
        response = None
        language = None
        language_removed = 0
        comments_removed = 0
        try:
            api_connection = new_connection(key)
            request = api_connection.videos().list(
                part="statistics, snippet", id=videos, maxResults=50, pageToken=page_token)

            response = request.execute()
            data = []
            items = response["items"]
            for item in items:
                video_id = item["id"]
                try:
                    statistics = item["statistics"]
                except KeyError:
                    statistics = None
                try:
                    view_count = statistics["viewCount"]
                except KeyError:
                    view_count = None
                try:
                    like_count = statistics["likeCount"]
                except KeyError:
                    like_count = None
                try:
                    comment_count = statistics["commentCount"]
                except KeyError:
                    comment_count = None

                snippet = item["snippet"]
                try:
                    title = snippet["title"]
                    try:
                        language = detect(title)
                    except:
                        print("Language detection error")
                except KeyError:
                    title = None
                try:
                    published_at = snippet["publishedAt"]
                except KeyError:
                    published_at = None
                try:
                    channel_id = snippet["channelId"]
                except KeyError:
                    channel_id = None

                try:
                    if language == "de":
                        if int(comment_count) > 0:
                            new_row = {'video_id': video_id, 'title': title, 'published_at': published_at, 'channel_id': channel_id,
                                       'view_count': view_count, 'like_count': like_count, 'comment_count': comment_count}

                            data.append(new_row)
                        else:
                            comments_removed = comments_removed + 1
                    else:
                        language_removed = language_removed + 1
                except TypeError as err:

                    print(err)

            return data, comments_removed, language_removed

        except HttpError as err:
            print(err)


def divide_chunks(videos, n):
    for i in range(0, len(videos), n):
        yield videos[i:i + n]


def main():
    file, filename = load_dataframe()

    video_file = file["video_id"].tolist()

    split_videos = list(divide_chunks(video_file, 50))

    key = input("Enter key: ")
    new_df = pd.DataFrame(
        columns=['video_id', 'title', 'published_at', 'channel_id', 'view_count', 'like_count', 'comment_count'])
    comments_removed = 0
    language_removed = 0
    for videos in split_videos:
        print(videos)
        data, comments, language = load_information(key, videos, filename)
        comments_removed = comments_removed + comments
        language_removed = language_removed + language
        print(data)
        new_df = new_df.append(data, ignore_index=True)

    save_dataframe(new_df, filename)
    print(f'{language_removed} removed because of language')
    print(f'{comments_removed} removed because of comments')


if __name__ == "__main__":
    main()
