from booklyb.utils.google_books_api_fetcher import fetch_book_information
from booklyb.error.not_found_error import ISBNNotFound

from booklyb.data.log import log, WARNING_MORE_THAN_ONE_RESULT_RETURNED
from booklyb.data.book_info import BookInfo
from booklyb.data.author import Author
from booklyb.data.publisher import Publisher

from booklyb.utils.import_size import metrics_size_to_mm

from datetime import datetime

MSG_WRN_MORE_THAN_ONE_RESULT_RETURNED = "Execpted one result but {} returned, first id take {} for procesing"


class GoogleBooksAPIFetcher:
    def fetch(self, isbn):
        book_raw_info = fetch_book_information(isbn)
        print(book_raw_info)
        if not book_raw_info:
            raise ISBNNotFound(f"Unable to find {isbn} isbn")

        # Retrive local and/or new authors
        authors = []
        authors_from_api = book_raw_info["authors"]

        for author_name in authors_from_api:
            authors_in_database = Author.find(name=author_name)
            if len(authors_in_database) >= 1:
                if len(authors_in_database) > 1:
                    log(code=WARNING_MORE_THAN_ONE_RESULT_RETURNED,
                        msg=MSG_WRN_MORE_THAN_ONE_RESULT_RETURNED.format(len(authors_in_database), authors_in_database[0].id),
                        authors=[str(a.id) for a in authors_in_database])
                authors.append(authors_in_database[0])
            else:
                authors.append(Author(name=author_name))

        # Retrive local and/or new publishers
        publishers = []
        publisher_name = book_raw_info["publisher"]

        publishers_in_database = Publisher.find(name=publisher_name)
        if len(publishers_in_database) >= 1:
            if len(publishers_in_database) > 1:
                log(code=WARNING_MORE_THAN_ONE_RESULT_RETURNED,
                    msg=MSG_WRN_MORE_THAN_ONE_RESULT_RETURNED.format(len(publishers_in_database), publishers_in_database[0].id),
                    publishers=[str(a.id) for a in publishers_in_database])
            publishers.append(publishers_in_database[0])
        else:
            publishers.append(Publisher(name=publisher_name))

        published_date = book_raw_info["publishedDate"]
        date_publisher_date = None

        if len(published_date) == 4:
            date_publisher_date = datetime.strptime(published_date, "%Y").date()
        elif len(published_date) == 7:
            date_publisher_date = datetime.strptime(published_date, "%Y-%m").date()
        elif len(published_date) == 10:
            date_publisher_date = datetime.strptime(published_date, "%Y-%m-%d").date()

        dimensions = book_raw_info["dimensions"]
        width = height = thickness = None

        if dimensions:
            width = metrics_size_to_mm(dimensions["width"])
            height = metrics_size_to_mm(dimensions["height"])
            thickness = metrics_size_to_mm(dimensions["thickness"])

        book_info = BookInfo(
            isbn=isbn,
            title=book_raw_info["title"],
            authors=authors,
            publishers=publishers,
            published_date=date_publisher_date,
            width_mm=width,
            thickness_mm=thickness,
            height_mm=height,
            page_count=book_raw_info["printedPageCount"],
            maturity_rating=book_raw_info["maturityRating"],
            language=book_raw_info["language"]
        )

        return book_info