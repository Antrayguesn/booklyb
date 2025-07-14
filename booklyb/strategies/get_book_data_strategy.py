from booklyb.strategies.strategy import Strategy

from booklyb.data.log import log, INFO_START_FETCHING_BOOK_DATA

from booklyb.fetchers.google_book_api_fetcher import GoogleBooksAPIFetcher
from booklyb.fetchers.local_database_fetcher import LocalDatabaseFetcher


class GetBookDataStrategy(Strategy):
    def load_data(self):
        self.book_data = None

    def write_data(self):
        pass

    def process(self, isbn):
        log(INFO_START_FETCHING_BOOK_DATA, f"Fetching data for isbn {isbn}", isbn=isbn)

        book_info = LocalDatabaseFetcher().fetch(isbn)
        if not book_info:
            book_info = GoogleBooksAPIFetcher().fetch(isbn)

        book_info.save()
        return book_info.to_dict()
