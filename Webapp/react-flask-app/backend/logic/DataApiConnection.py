import googleapiclient.discovery


class DataApiConnection:
    def __init__(self, key):
        self.api_connection = None
        self.key = key

    def new_connection(self):
        api_service_name = "youtube"
        api_version = "v3"
        api_connection = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=self.key)

        self.api_connection = api_connection

    def get_video_info(self, search_query, published_before, published_after):
        page_token = ""

        while page_token is not None:
            kind = []
            result_id = []

            request = self.api_connection.search().list(
                part="id", q=search_query, maxResults=50, pageToken=page_token, publishedAfter=published_after,
                publishedBefore=published_before, fields="items()"
            )

            response = request.execute()

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
            data = {'kind': kind, 'result_id': result_id}
            # Save each badge to database
            print(data)
