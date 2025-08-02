from datetime import datetime


def date_formater(published_date: str) -> float:
    date_publisher_date = None
    if published_date is not None:
        if len(published_date) == 4:
            date_publisher_date = datetime.strptime(published_date, "%Y")
        elif len(published_date) == 7:
            date_publisher_date = datetime.strptime(published_date, "%Y-%m")
        elif len(published_date) == 10:
            date_publisher_date = datetime.strptime(published_date, "%Y-%m-%d")

    published_date_timestamp = None
    if date_publisher_date:
        published_date_timestamp = date_publisher_date.timestamp()
    else:
        print("**************")
        print(published_date)
        print("**************")


    return published_date_timestamp
