import datetime

from logic.DataApiConnection import DataApiConnection

key = "AIzaSyDVseWOuiO1diHvWYZ0-76WM0RKEWo4DgE"

connection = DataApiConnection(key)

DataApiConnection.new_connection(connection)

search_query = "E-"

published_before = datetime.datetime(2022, 1, 2).isoformat("T") + "Z"
published_after = datetime.datetime(2022, 1, 1).isoformat("T") + "Z"
print(published_after)

DataApiConnection.get_video_info(connection, search_query, published_before, published_after)
