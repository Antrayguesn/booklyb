from booklyb.utils.google_books_api_fetcher import fetch_book_information
from booklyb.error.not_found_error import ISBNNotFound

from booklyb.data.log import log
from booklyb.data.book_info import BookInfo

from booklyb.utils.import_size import metrics_size_to_mm
from booklyb.utils.date_formater_utils import date_formater

# TODO Add a data for


class GoogleBooksAPIFetcher:
    RATE_LIMIT = 1000
    # One day in second
    RATE_TIME_LIMIT = 24 * 60 * 60

    TRUST_INDICE = 10

    def fetch(self, isbn):
        book_raw_info = fetch_book_information(isbn, fetcher_name=self.__class__.__name__)

        # if you search for a isbn that not exist and next by another one that exist
        #  google book api will return the existing one
        # if you lookup for 9782811215058 google book api return data for 9782811215057
        # 9782811215060 for 9782811215064
        if not book_raw_info:
            raise ISBNNotFound(f"Unable to find {isbn} isbn")
        try:
            industryID = [value[1] for key, value in [v.items() for v in book_raw_info["industryIdentifiers"]]]
        except KeyError:
            log("ERROR_0003", "Key industryIdentifiers.type.ISBN_13 not found on google api books return")
            raise ISBNNotFound(f"Unable to find {isbn} isbn")

        if isbn not in industryID:
            log("ERROR_0005", f"ISBN {isbn} no matching with google api book return : {",".join(industryID)}", isbn=isbn, industryID=str(industryID))
            raise ISBNNotFound(f"Unable to find {isbn} isbn")

        # Retrive local and/or new authors
        authors_from_api = book_raw_info.get("authors", [])

        # Retrive local and/or new publishers
        publisher_name = book_raw_info.get("publisher", [])

        published_date = book_raw_info.get("publishedDate", None)
        published_date_timestamp = date_formater(published_date)

        dimensions = book_raw_info.get("dimensions", None)
        width = height = thickness = None

        if dimensions:
            width = metrics_size_to_mm(dimensions["width"])
            height = metrics_size_to_mm(dimensions["height"])
            thickness = metrics_size_to_mm(dimensions["thickness"])

        book_info = BookInfo(
            isbn=isbn,
            title=book_raw_info.get("title", None),
            published_date=published_date_timestamp,
            width_mm=width,
            thickness_mm=thickness,
            height_mm=height,
            page_count=book_raw_info.get("printedPageCount", None),
            target_audience=book_raw_info.get("maturityRating", None),
            language=book_raw_info.get("language", None),
            description=book_raw_info.get("description", None),
            fetcher_name=self.__class__.__name__
        )

        book_info.add_authors(authors_from_api)
        book_info.add_publisher(publisher_name)

        return book_info
