from datetime import datetime
date = "2022-02-18T16:50:59Z"

date = date[:-1]
date_new = datetime.fromisoformat(date)

print(date_new)
#datetime.datetime(2020, 1, 6, 0, 0, tzinfo=datetime.timezone.utc)