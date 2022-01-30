import datetime

from logic.YouTubeDataApi import YouTubeDataApi


def test(db):
    key = "AIzaSyDVseWOuiO1diHvWYZ0-76WM0RKEWo4DgE"

    connection = YouTubeDataApi(key, db)

    YouTubeDataApi.new_connection(connection)

    search_query = "E-"

    published_before = datetime.datetime(2022, 1, 2).isoformat("T") + "Z"
    published_after = datetime.datetime(2022, 1, 1).isoformat("T") + "Z"
    print(published_after)

    YouTubeDataApi.execute_search_query(connection, search_query, published_before, published_after)
