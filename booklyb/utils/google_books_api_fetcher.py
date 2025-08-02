from booklyb.data.log import log

from booklyb.utils.request_utils import request_url

from booklyb.error.not_found_error import ISBNNotFound

GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes?q=isbn:{}"


def fetch_book_information(isbn: str, fetcher_name: str = None):
    resp = request_url(GOOGLE_BOOKS_API.format(isbn), fetcher_name=fetcher_name)
    books_info = resp.json()

    if books_info["totalItems"] == 0:
        log("INFO_9999", f"No book found for isbn {isbn}", isbn=isbn)
        raise ISBNNotFound(f"No book found for isbn {isbn}")

    book_link = books_info["items"][0]["selfLink"]

    resp = request_url(book_link, fetcher_name=fetcher_name)
    book_info = resp.json()
    volume_info = book_info["volumeInfo"]
    return volume_info
