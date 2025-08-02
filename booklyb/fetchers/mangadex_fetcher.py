from booklyb.data.book_info import BookInfo

from booklyb.utils.date_formater_utils import date_formater
from booklyb.utils.bnf_api_utils import fetch_book_information

from booklyb.data.log import log


MSG_WRN_MORE_THAN_ONE_RESULT_RETURNED = "Execpted one result but {} returned, first id take {} for procesing"


# TODO Add a data for

class MangaDexFetcher:
    RATE_LIMIT = 10000
    # One day in second
    RATE_TIME_LIMIT = 24 * 60 * 60

    TRUST_SCORE = 1

    def fetch(self, isbn):
        log("INFO_0002", f"Fetching with {self.__class__.__name__} for isbn {isbn}", isbn=isbn)
        book_data = fetch_book_information(isbn)

        print(book_data)

        title_informations = book_data.get(self.TITLE_INFORMATIONS, {})

        title = title_informations.get(self.TITLE_LABEL, None)
        name_of_part = title_informations.get(self.NAME_OF_PART, None)
        number_of_part = title_informations.get(self.NUMBER_OF_PART, None)
        author_name = title_informations.get(self.AUTHOR_NAME, None)

        description = book_data.get(self.SUMMARY, {}).get(self.TEXT_OF_NOTE, None)

        general_data = book_data.get(self.GENERAL_DATA, {})
        target_audience = general_data.get(self.TARGET_AUDIENCE, None)

        publisher_data = book_data.get(self.PUBLISHER_DATA, {})
        publisher_name = publisher_data.get(self.PUBLISHER_NAME, None)
        published_date = publisher_data.get(self.DATE_OF_PUBLICATION, None)

        set_data = book_data.get(self.SET, {})

        serie_name = set_data.get(self.TITLE, None)
        volume_number = set_data.get(self.VOLUME_NUMBER, None)

        if name_of_part is None and serie_name and title and title != serie_name:
            name_of_part = title
            title = serie_name

        if number_of_part is None and volume_number:
            number_of_part = volume_number

        try:
            published_date_timestamp = date_formater(published_date)
        except ValueError:
            published_date_timestamp = None

        text_language = book_data.get(self.LANGUAGE, {}).get(self.TEXT_LANGUAGE, None)

        book_info = BookInfo(
            isbn=isbn,
            title=title,
            subtitle=name_of_part,
            volume_number=number_of_part,
            published_date=published_date_timestamp,
            target_audience=", ".join(target_audience),
            language=text_language,
            serie=serie_name,
            description=description,
        )

        book_info.add_authors([author_name])
        book_info.add_publisher(publisher_name)

        return book_info
